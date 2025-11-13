from lmdeploy import pipeline, TurbomindEngineConfig, ChatTemplateConfig
from lmdeploy.vl import load_image
import torch
# 初始化全局对象（只加载一次）
model = 'OpenGVLab/InternVL3-8B'
backend_config = TurbomindEngineConfig(session_len=16384, tp=1,do_rescale=False,torch_dtype=torch.bfloat16)
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