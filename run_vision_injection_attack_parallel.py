# visprog_editing_attack.py  —— 替换你的 main + 调度
import json, os, re, argparse, multiprocessing as mp
from PIL import Image
import torch
from torchvision import transforms
from tqdm import tqdm
from multimodal_injection import MultimodalInjection
from program_generator import ProgramGenerator
from prompts.imgedit import PROMPT
import os

os.environ["HF_HOME"] = "/datasets/work/d61-ai-security/work/cha818/huggingface_cache"
os.environ["TRANSFORMERS_CACHE"] = "/datasets/work/d61-ai-security/work/cha818/huggingface_cache"
os.environ["TORCH_HOME"] = "/datasets/work/d61-ai-security/work/cha818/torch_cache"

lvlm_to_module = {
    "gpt4": "load_GPT4o",
    "gpt5": "load_GPT5",
    "llava": "load_LLaVA",
    "minigpt4": "load_MiniGPT4",
    "deepseek": "load_deepseek",
    "qwenvl": "load_Qwen_VL",
    "gemini": "load_gemini",
    "claude": "load_claude",
    "internvl": "load_internvl",
}

def create_prompt(instruction):
    return PROMPT.format(instruction=instruction)

def extract_program_text(plan: str):
    m = re.search(r"```(?:python|plaintext)?[\n\\]+(.*?)```", plan, re.DOTALL)
    return m.group(1).strip() if m else plan.strip()

def _worker(rank, gpu_id, items, image_dir, attack_type, lvlm_name, tmp_dir, result_list, partial_json):

    if not attack_type.startswith("noise"):
        generator = ProgramGenerator(prompter=create_prompt, lvlm=lvlm_to_module[lvlm_name])

    attacker = MultimodalInjection(attack_type, device=gpu_id) 
    os.makedirs(tmp_dir, exist_ok=True)
    partial_data = []
    def flush_partial():
        merged_map = {}
        for e in partial_data:
            if isinstance(e, dict) and "idx" in e:
                merged_map[e["idx"]] = e
        ordered = [merged_map[k] for k in sorted(merged_map.keys())]
        os.makedirs(os.path.dirname(partial_json), exist_ok=True)
        with open(partial_json, "w") as f:
            json.dump(ordered, f, indent=2)

    to_pil = transforms.ToPILImage()
    for (orig_idx, entry) in items:
        image_path = os.path.join(image_dir, entry["image"])
        if not os.path.exists(image_path):
            print(f"[GPU{gpu_id}][Skip] Image not found: {image_path}")
            continue

        # try:
        if not attack_type.startswith("noise"):
            attacked_image = attacker.apply(image_path, entry["attack_instuction"])
            attacked_image_path = os.path.join(tmp_dir, f"attacked_temp_{orig_idx}.jpg")
            attacked_image.save(attacked_image_path)
            plan, _ = generator.mm_generate(entry["user_instruction"], attacked_image_path)
            program = extract_program_text(plan)
        else:
            plan, attacked_tensor = attacker.apply(
                image_path, entry["attack_instuction"], attack_context=entry
            )
            attacked_image = to_pil(attacked_tensor.squeeze(0).cpu())
            attacked_image_path = os.path.join(tmp_dir, f"attacked_temp_{orig_idx}.jpg")
            attacked_pth_path  = os.path.join(tmp_dir, f"attacked_temp_{orig_idx}.pth")

            torch.save(attacked_tensor.detach().cpu(), attacked_pth_path)
            attacked_image.save(attacked_image_path)
            program = extract_program_text(plan)

        entry[f"plan_with_{attack_type.lower().replace(' ', '_')}"] = program
        entry_with_idx = dict(entry)
        entry_with_idx["idx"] = orig_idx

        result_list.append((orig_idx, entry_with_idx))
        partial_data.append(entry_with_idx)

        flush_partial() 

        print(f"[GPU{gpu_id}] OK #{orig_idx} -> {entry['image']}")


def attack_visprog_editing_parallel(input_json, image_dir, output_json, output_folder,attack_type, devices, workers, lvlm_name, start_idx=0, limit=None):
    with open(input_json, "r") as f:
        dataset = json.load(f)

    
    start = max(0, int(start_idx))
    end = len(dataset) if limit is None else min(len(dataset), start + int(limit))
    subset = dataset[start:end]
    
    world_size = min(workers, len(devices)) if workers > 0 else len(devices)
    print(world_size)
    print(devices)
    shards = [[] for _ in range(world_size)]
    for idx, entry in enumerate(subset, start=start):
        shards[idx % world_size].append((idx, entry))

    manager = mp.Manager()
    results = manager.list()
    procs = []
    
    print(shards)

    for rank in range(world_size):
        gpu_id = devices[rank]
        print('helllo', gpu_id)
        tmp_dir = os.path.join(f"/datasets/work/d61-ai-security/work/cha818/visprog/{output_folder}" if attack_type.startswith("noise") else "/datasets/work/d61-ai-security/work/cha818/visprog/tmp",f"gpu{gpu_id}")
        partial_json = os.path.join(f"/datasets/work/d61-ai-security/work/cha818/visprog/{output_folder}" if attack_type.startswith("noise") else "/datasets/work/d61-ai-security/work/cha818/visprog/tmp", f"partial_gpu{gpu_id}.json")
        p = mp.Process(
            target=_worker,
            args=(rank, gpu_id, shards[rank], image_dir, attack_type, lvlm_name, tmp_dir, results, partial_json),
            daemon=False,
        )
        p.start()
        procs.append(p)

    for p in procs:
        p.join()

    results = list(results)
    results.sort(key=lambda x: x[0])
    merged = [entry for _, entry in results]
    merged_map = {e.get("idx"): e for e in merged if isinstance(e, dict) and "idx" in e}

    if os.path.isdir(tmp_dir):
        for fn in os.listdir(tmp_dir):
            if not fn.endswith(".json"):
                continue
            pth = os.path.join(tmp_dir, fn)
            try:
                with open(pth, "r") as f:
                    part = json.load(f)
                for e in part:
                    if isinstance(e, dict) and "idx" in e:
                        merged_map[e["idx"]] = e  # 以局部文件为准
            except Exception:
                pass

    merged_full = [merged_map[k] for k in sorted(merged_map.keys())]
    with open(output_json, "w") as f:
        json.dump(merged_full, f, indent=2)


if __name__ == "__main__":
    mp.set_start_method("spawn", force=True) 
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_json", type=str, required=True)
    parser.add_argument("--image_dir", type=str, required=True)
    parser.add_argument("--output_json", type=str, required=True)
    parser.add_argument("--output_folder", type=str, required=True)
    parser.add_argument("--attack_type", type=str, required=True,
                        choices=["naive","ignore","completion","combine","warning","noise","noise_robust","noise_lpips","noise_lpips_robust","noise_blackbox","noise_blackbox_robust","noise_lpips_blackbox","noise_lpips_blackbox_robust"])
    parser.add_argument("--lvlm", type=str, default="gpt4", choices=lvlm_to_module.keys())
    parser.add_argument("--devices", type=str, default="0,")
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--start_idx", type=int, default=0)
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()

    devices = [int(x) for x in args.devices.split(",") if x.strip()!=""]
    attack_visprog_editing_parallel(
        args.input_json, args.image_dir, args.output_json, args.output_folder,
        args.attack_type, devices, args.workers, args.lvlm, start_idx = args.start_idx, limit = args.limit
    )
