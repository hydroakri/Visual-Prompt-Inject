# Import the Python SDK
import google.generativeai as genai
# Used to securely store your API key
from PIL import Image 

GOOGLE_API_KEY=""
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel("gemini-2.5-pro")


def gen_with_model(img, prompt):
    try:
        response = model.generate_content([img, prompt])
        
        return response.text
    except Exception as e:
        print(f"Error generating content with Gemini model: {e}")
        return "None"

def call_model(img, prompt):
    
    return gen_with_model(Image.open(img), prompt), None  # No logprobs available





# model = genai.GenerativeModel(
#     "gemini-2.5-pro",
#     generation_config={
#         "max_output_tokens": 1024,
#         "temperature": 0.3,
#         "response_mime_type": "text/plain",  # 关键：强制纯文本
#     },
#     # 如果你没有用工具调用，就不要传 tools；否则模型可能只返回 function_call 而无 text
#     # tools=[...]
# )


# def gen_with_model(img_path, prompt):
#     import base64
#     img_b64 = base64.b64encode(open(img_path, "rb").read()).decode("utf-8")
#     image_part = {"inline_data": {"mime_type": "image/jpeg", "data": img_b64}}
#     resp = model.generate_content([image_part, prompt])

#     # 调试打印

#     # 提取文本
#     texts = [p.text for p in resp.candidates[0].content.parts if hasattr(p, "text")]
#     print(texts)
#     return "\n".join(texts) if texts else None

# def call_model(img_path: str, prompt: str):
#     # 与你原函数兼容
#     return gen_with_model(img_path, prompt), None  # 无 logprobs
