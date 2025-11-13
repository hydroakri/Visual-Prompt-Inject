import torch
from transformers import AutoModelForCausalLM
from deepseek_vl.models import VLChatProcessor, MultiModalityCausalLM
from deepseek_vl.utils.io import load_pil_images
import tqdm
import random
import json


model_path = "deepseek-ai/deepseek-vl-7b-chat"
vl_chat_processor: VLChatProcessor = VLChatProcessor.from_pretrained(model_path)
tokenizer = vl_chat_processor.tokenizer

vl_gpt: MultiModalityCausalLM = AutoModelForCausalLM.from_pretrained(model_path, trust_remote_code=True)
vl_gpt = vl_gpt.to(torch.bfloat16).cuda().eval()


def call_model(image_path, query):
    conversation = [
        {
            "role": "User",
            "content": f"<image_placeholder>{query}",
            "images": [image_path],
        },
        {"role": "Assistant", "content": ""},
    ]
    pil_images = load_pil_images(conversation)
    prepare_inputs = vl_chat_processor(
        conversations=conversation,
        images=pil_images,
        force_batchify=True
    ).to(vl_gpt.device)

    inputs_embeds = vl_gpt.prepare_inputs_embeds(**prepare_inputs)

    outputs = vl_gpt.language_model.generate(
        inputs_embeds=inputs_embeds,
        attention_mask=prepare_inputs.attention_mask,
        pad_token_id=tokenizer.eos_token_id,
        bos_token_id=tokenizer.bos_token_id,
        eos_token_id=tokenizer.eos_token_id,
        max_new_tokens=512,
        do_sample=False,
        use_cache=True
    )

    answer = tokenizer.decode(outputs[0].cpu().tolist(), skip_special_tokens=True)
    prob = None  # No logprobs available
    return answer,prob

def call_model_tensor(image_tensor, query):
    """
    调用 DeepSeek-VL 模型，输入为图像 tensor 或 PIL.Image。
    参数:
        image_tensor: torch.Tensor 或 PIL.Image
            - 如果是 Tensor: 形状可以是 (C,H,W) 或 (H,W,C)，数值范围 [0,1] 或 [0,255]
        query: str, 用户问题
    返回:
        answer: 模型生成的回答文本
        prob: None（此模型不返回概率）
    """
    from PIL import Image
    import torchvision.transforms as T

    # 确保输入是 PIL.Image
    image_tensor = image_tensor[0]
    print(image_tensor.shape)
    if isinstance(image_tensor, torch.Tensor):
        if image_tensor.dim() == 3:
            if image_tensor.max() <= 1:
                image_tensor = image_tensor * 255
            image_tensor = image_tensor.byte()
            if image_tensor.shape[0] in [1, 3]:  # CHW → HWC
                image_tensor = image_tensor.permute(1, 2, 0)
            image_tensor = Image.fromarray(image_tensor.cpu().numpy())
        else:
            raise ValueError("image_tensor must have 3 dimensions (C,H,W) or (H,W,C)")
    elif not isinstance(image_tensor, Image.Image):
        raise TypeError("image_tensor must be a torch.Tensor or PIL.Image")

    # 构造输入对话
    conversation = [
        {
            "role": "User",
            "content": f"<image_placeholder>{query}",
            "images": [image_tensor],
        },
        {"role": "Assistant", "content": ""},
    ]

    # 直接用已加载的 image_tensor（无需路径）
    pil_images = [image_tensor]
    prepare_inputs = vl_chat_processor(
        conversations=conversation,
        images=pil_images,
        force_batchify=True
    ).to(vl_gpt.device)

    inputs_embeds = vl_gpt.prepare_inputs_embeds(**prepare_inputs)

    outputs = vl_gpt.language_model.generate(
        inputs_embeds=inputs_embeds,
        attention_mask=prepare_inputs.attention_mask,
        pad_token_id=tokenizer.eos_token_id,
        bos_token_id=tokenizer.bos_token_id,
        eos_token_id=tokenizer.eos_token_id,
        max_new_tokens=512,
        do_sample=False,
        use_cache=True
    )

    answer = tokenizer.decode(outputs[0].cpu().tolist(), skip_special_tokens=True)
    return answer, None