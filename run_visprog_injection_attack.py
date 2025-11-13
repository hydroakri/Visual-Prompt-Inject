import os
import re
import json
import torch
import argparse
from PIL import Image
from tqdm import tqdm
from torchvision import transforms

from multimodal_injection import MultimodalInjection
from transformers import AutoProcessor, AutoModelForImageTextToText
from vis_prog_engine.utils import ProgramGenerator

from torchvision import transforms
to_pil = transforms.ToPILImage()
from prompts.embodied import PROMPT as PROMPT_EMBODIED
from prompts.imgedit import PROMPT as PROMPT_IMGEDIT

def create_prompt_embodied(instruction):
        return PROMPT_EMBODIED.format(instruction=instruction)
def create_prompt_edit(instruction):
        return PROMPT_IMGEDIT.format(instruction=instruction)
    



def extract_program_text(plan: str):
    match = re.search(r"```(?:python|plaintext)?[\n\\]+(.*?)```", plan, re.DOTALL)
    if match:
        return match.group(1).strip()
    return plan.strip()


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


def attack_visprog_editing(input_json, image_dir, output_json, attack_type,cache_dir, mode): 
    if mode == "embodied":
        create_prompt = create_prompt_embodied
    else:
        create_prompt = create_prompt_edit
    print(lvlm_to_module[args.lvlm])
    if not attack_type.startswith("noise") or cache_dir is None:
        generator = ProgramGenerator(
            prompter=create_prompt,
            lvlm=lvlm_to_module[args.lvlm]
        )
    if cache_dir is not None:
        generator = ProgramGenerator(
            prompter=create_prompt,
            lvlm=lvlm_to_module[args.lvlm],
            tensor=True
        )
    
    with open(input_json, 'r') as f:
        dataset = json.load(f)
    if cache_dir is None:
        attacker = MultimodalInjection(attack_type)
    new_data = []
    if not os.path.exists(f"/bowen/d61-ai-security/work/cha818/visprog/attack_sample/{attack_type}"):
        os.makedirs(f"/bowen/d61-ai-security/work/cha818/visprog/attack_sample/{attack_type}")

    for i, entry in enumerate(dataset):
        image_path = os.path.join(image_dir, entry['image'])
        if not os.path.exists(image_path):
            print(f"[Warning] Image not found: {image_path}")
            continue
        
        if cache_dir is not None:
            cached_pth = os.path.join(cache_dir, f"attacked_temp_{i}.pth")
            attacked_tensor = torch.load(cached_pth)  
            plan, _ = generator.mm_generate(entry["user_instruction"], attacked_tensor)
            program = extract_program_text(plan)
            print(program)
            entry[f"plan_with_{attack_type.lower().replace(' ', '_')}"] = program
            new_data.append(entry)
            continue
        if attack_type == "random_noise":
            image = Image.open(image_path).convert("RGB")
            noise = torch.randn_like(transforms.ToTensor()(image)) * 0.16
            attacked_tensor = transforms.ToTensor()(image) + noise
            attacked_tensor = attacked_tensor.unsqueeze(0)
            print(attacked_tensor.shape)
            
            plan, _ = generator.mm_generate(entry["user_instruction"], attacked_tensor)
            program = extract_program_text(plan)
            print(program)
            entry[f"plan_with_{attack_type.lower().replace(' ', '_')}"] = program
            new_data.append(entry)
            continue

        if not attack_type.startswith("noise"):
            attacked_image = attacker.apply(image_path, entry['attack_instuction'])
            
            attacked_image_path = os.path.join(
                f"/bowen/d61-ai-security/work/cha818/visprog/attack_sample/{attack_type}",
                f"attacked_temp_{i}.jpg"
            )
            attacked_image.save(attacked_image_path)
            print(attacked_image_path)

            plan, _ = generator.mm_generate(entry['user_instruction'], attacked_image_path)
            program = extract_program_text(plan)
        else:
            plan, attacked_image_tensor = attacker.apply(
                image_path,
                entry['attack_instuction'],
                attack_context=entry
            )
            attacked_image = transforms.ToPILImage()(attacked_image_tensor.squeeze(0).cpu())

            attacked_image_path = os.path.join(
                "/bowen/d61-ai-security/work/cha818/visprog/noised",
                f"attacked_temp_{i}.jpg"
            )
            attacked_pth_path = os.path.join(
                "/bowen/d61-ai-security/work/cha818/visprog/noised",
                f"attacked_temp_{i}.pth"
            )

            torch.save(attacked_image_tensor.detach().cpu(), attacked_pth_path)
            attacked_image.save(attacked_image_path)
            print(attacked_image_path)

            program = extract_program_text(plan)

        print(program)
        entry[f"plan_with_{attack_type.lower().replace(' ', '_')}"] = program
        print(f"[Success] Generated plan '{entry['user_instruction']}' for {entry['image']}")
        new_data.append(entry)

    with open(output_json, 'w') as f:
        json.dump(new_data, f, indent=2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_json', type=str, required=True)
    parser.add_argument('--image_dir', type=str, required=True)
    parser.add_argument('--output_json', type=str, required=True)
    parser.add_argument('--attack_type', type=str, required=True, choices=[
        "random_noise","naive", "ignore", "completion", "combine", "combinepro","warning", "emoji","noise","noise_lpips","noise_whitebox","noise_lpips_whitebox","noise_robust","noise_lpips_robust","noise_whitebox_robust","noise_lpips_whitebox_robust"
    ])
    parser.add_argument('--lvlm', type=str, default="gpt4", choices=lvlm_to_module.keys())
    parser.add_argument("--cache_dir", type=str, default=None)
    parser.add_argument("--mode", type=str, required=False, default="imgedit", choices=["embodied", "imgedit"])
    args = parser.parse_args()

    attack_visprog_editing(args.input_json, args.image_dir, args.output_json, args.attack_type,args.cache_dir,args.mode)
