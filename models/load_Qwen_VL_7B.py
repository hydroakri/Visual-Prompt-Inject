from transformers import Qwen2_5_VLForConditionalGeneration, AutoTokenizer, AutoProcessor,AutoModelForImageTextToText, BitsAndBytesConfig
from transformers.generation import GenerationConfig
import torch
from transformers import AutoModel, GenerationConfig
from transformers.generation import GenerationConfig
from qwen_vl_utils import process_vision_info
import torch
import json
import tqdm
import random
from PIL import Image
from torchvision import transforms
torch.manual_seed(1234)
from PIL import Image

import torch


tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-VL-7B-Instruct", trust_remote_code=True)
device = "cuda:0" if torch.cuda.is_available() else "cpu"

model = AutoModelForImageTextToText.from_pretrained(
            "Qwen/Qwen2.5-VL-7B-Instruct",
            device_map="auto",
            max_memory={0: "5GiB", "cpu": "24GiB"},
            quantization_config=BitsAndBytesConfig(
                load_in_8bit=True,
                llm_int8_enable_fp32_cpu_offload=True,
            ),
            trust_remote_code=True
        )
processor = AutoProcessor.from_pretrained("Qwen/Qwen2.5-VL-7B-Instruct")
model.generation_config = GenerationConfig.from_pretrained("Qwen/Qwen2.5-VL-7B-Instruct", trust_remote_code=True)

# Function to generate caption with grounding
def call_model(image_path, text_prompt):
    image = Image.open(image_path).convert("RGB")
    transform = transforms.ToTensor()
    orig_tensor = transform(image).unsqueeze(0)
    pixel_tensor = orig_tensor.clone().requires_grad_(True)

    messages = [{
        "role": "user",
        "content": [
            {"type": "image","image": image},
            {"type": "text", "text": text_prompt},
        ]}]

    text = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    image_inputs, video_inputs = process_vision_info(messages)

    inputs = processor(
        text=[text],
        images=pixel_tensor,
        padding=True,
        return_tensors="pt",
        do_rescale=False,
    )

    inputs = inputs.to("cuda")

    # Inference: Generation of the output
    generated_ids = model.generate(**inputs, max_new_tokens=128)
    generated_ids_trimmed = [
        out_ids[len(in_ids) :] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
    ]
    output_text = processor.batch_decode(
        generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
    )
    return output_text[0], None


def call_model_tensor(image_tensor, text_prompt):
    eval_prompt_text = processor.apply_chat_template(
        [{"role": "user", "content": [
            {"type": "image", "image": None},
            {"type": "text", "text": text_prompt}
        ]}],
        tokenize=False, add_generation_prompt=True
    )

    gen_inputs = processor(
        images=image_tensor,
        text=eval_prompt_text,
        return_tensors="pt",
        do_rescale=False
    ).to(device)
    tokenizer = processor.tokenizer


    # Inference: Generation of the output
    gen_ids = model.generate(
        input_ids=gen_inputs["input_ids"],
        attention_mask=gen_inputs.get("attention_mask"),
        pixel_values=gen_inputs["pixel_values"],
        image_grid_thw=gen_inputs["image_grid_thw"],
        max_new_tokens=256,
        pad_token_id=tokenizer.eos_token_id
    )
    generated_ids_trimmed = [
        out_ids[len(in_ids) :] for in_ids, out_ids in zip(gen_inputs["input_ids"], gen_ids)
    ]
    output_text = processor.batch_decode(
        generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
    )
    return output_text[0], None
