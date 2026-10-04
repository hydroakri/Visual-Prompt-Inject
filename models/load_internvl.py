from lmdeploy import pipeline, TurbomindEngineConfig, ChatTemplateConfig
from lmdeploy.vl import load_image
import torch
# 初始化全局对象（只加载一次）
# NOTE 2026-09-22: correctly configured (AWQ checkpoint + model_format='awq'), but confirmed
# OOMs on this project's 6GB RTX 3060 Laptop even at session_len=2048/cache_max_entry_count=0.05
# -- the AWQ checkpoint itself is ~5.9GB on disk (4x pytorch_model.bin shards + fp16 vision
# tower), which already exceeds free VRAM before any KV cache is allocated. This is a
# weight-loading OOM, not a cache-sizing one, so no amount of session_len/cache tuning fixes it
# on this hardware. See docs/progress/2026-09-22-internvl-baseline-attempt.md. Should work as-is
# on a GPU with more headroom (e.g. the project's eventual desktop/Jetson stages).
model = 'OpenGVLab/InternVL3-8B-AWQ'
backend_config = TurbomindEngineConfig(model_format='awq', session_len=2048, tp=1, cache_max_entry_count=0.05, quant_policy=4)
chat_template_config = ChatTemplateConfig(model_name='internvl2_5')
pipe = pipeline(model, backend_config=backend_config, chat_template_config=chat_template_config)

def call_model(image_path_or_url, query):
    """
    调用 InternVL3-8B 模型生成图文回答

    Args:
        image_path_or_url (str): 本地路径或网络URL
        query (str): 用户查询文本

    Returns:
        str: 模型生成的文本结果
    """
    image = load_image(image_path_or_url)
    response = pipe((query, image))
    return response.text, None


def call_model_tensor(image_tensor, query):
    """
    Assumes image_tensor is a torch tensor of shape (1, 3, H, W), values in [0, 1].
    Converts to PIL for InternVL3 pipeline compatibility.
    """
    assert isinstance(image_tensor, torch.Tensor)


    response = pipe((query, image_tensor))
    return response.text, None