import os
import json
import argparse
import re
from PIL import Image
from vis_prog_engine.utils import ProgramGenerator

from prompts.embodied import PROMPT as PROMPT_EMBODIED
from prompts.imgedit import PROMPT as PROMPT_IMGEDIT


def extract_program_text(plan):
    match = re.search(r"```(?:python|plaintext)?[\n\\]+(.*?)```", plan, re.DOTALL)
    if match:
        return match.group(1).strip()
    return plan.strip()

def create_prompt_embodied(instruction):
        return PROMPT_EMBODIED.format(instruction=instruction)
def create_prompt_edit(instruction):
        return PROMPT_IMGEDIT.format(instruction=instruction)

lvlm_to_module = {
    "gpt4": "load_GPT4o",
    "gpt5": "load_GPT5",
    "llava": "load_LLaVA",
    "minigpt4": "load_MiniGPT4",
    "deepseek": "load_deepseek",
    'qwenvl': 'load_Qwen_VL',
    "gemini": "load_gemini",
    "claude": "load_claude",
    "internvl": "load_internvl",
}

def main(args):
    if args.mode == "embodied":
        generator = ProgramGenerator(prompter=create_prompt_embodied, lvlm=lvlm_to_module[args.lvlm])
    else:
        generator = ProgramGenerator(prompter=create_prompt_edit, lvlm=lvlm_to_module[args.lvlm])

    with open(args.input_json, 'r') as f:
        data = json.load(f)

    updated_data = []
    user_plan_cache = {}  # {(image, user_instruction): user_plan}

    for item in data:
        print(item)
        image_path = os.path.join(args.image_dir, item["image"])
        if not os.path.exists(image_path):
            print(f"[Warning] Image not found: {image_path}")
            continue

        # 生成或复用 user_plan
        user_key = (item["image"], item["user_instruction"])
        if user_key not in user_plan_cache:
            try:
                new_user_plan, _ = generator.mm_generate(item["user_instruction"], image_path)
                user_plan_cache[user_key] = extract_program_text(new_user_plan)
                print(f"[Info] Generated user_plan for {item['image']}, instruction: {item['user_instruction']}")
            except Exception as e:
                print(f"[Error] Failed to generate user_plan for {item['image']}: {e}")
                continue

        item["user_plan"] = user_plan_cache[user_key]

        # 单独生成 attack_plan（不缓存）
        try:
            new_attack_plan, _ = generator.mm_generate(item["attack_instuction"], image_path)
            item["attack_plan"] = extract_program_text(new_attack_plan)
            print(f"[Success] Updated attack_plan for image: {item['image']} | goal: {item['attack_goal']}")
        except Exception as e:
            print(f"[Error] Failed to generate attack_plan for {item['image']}: {e}")
            continue

        updated_data.append(item)

        # print(f"[Error] Failed to process {item['image']}: {str(e)}")

    with open(args.output_json, 'w') as f:
        json.dump(updated_data, f, indent=2)
    print(f"[Done] Output saved to {args.output_json}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_json", required=True, help="Input JSON file")
    parser.add_argument("--image_dir", required=True, help="Directory of image files")
    parser.add_argument("--output_json", required=True, help="Output JSON file with new lvlm plans")
    parser.add_argument("--lvlm", type=str, required=True, choices=lvlm_to_module.keys())
    parser.add_argument("--mode", type=str, required=False, default="imgedit", choices=["embodied", "imgedit"])
    args = parser.parse_args()
    main(args)
