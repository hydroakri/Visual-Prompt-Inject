import base64
from mimetypes import guess_type
import openai

# Talks to a local llama.cpp `llama-server` instance running InternVL3-2B
# (GGUF, Q4_K_M + mmproj vision encoder) on port 8084 -- started separately, ad hoc,
# same recipe as models/load_Qwen_VL_7B_gguf.py (port 8082) and
# models/load_InternVL3_8B_gguf.py (port 8083). See
# docs/progress/2026-09-22-internvl-baseline-attempt.md for the --no-mmproj-offload fix.
client = openai.OpenAI(base_url="http://127.0.0.1:8084/v1", api_key="not-needed")


def local_image_to_data_url(image_path):
    mime_type, _ = guess_type(image_path)
    if mime_type is None:
        mime_type = 'application/octet-stream'
    with open(image_path, "rb") as image_file:
        base64_encoded_data = base64.b64encode(image_file.read()).decode('utf-8')
    return base64_encoded_data


def call_model(image_path, prompt):
    try:
        response = client.chat.completions.create(
            model="internvl3-2b",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that generates visual editing programs from image and instruction."
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{local_image_to_data_url(image_path)}"}}
                    ]
                }
            ],
            temperature=0.7,
            max_tokens=512,
            top_p=0.5,
            frequency_penalty=0,
            presence_penalty=0,
        )
        prog = response.choices[0].message.content.strip()
        prob = None  # No logprobs available
        return prog, prob
    except Exception as e:
        print(f"Error calling model: {e}")
        return "None", None


def call_model_tensor(image_tensor, prompt):
    image_path = "/tmp/internvl2b_gguf_temp.jpg"
    from torchvision import transforms
    attacked_image = transforms.ToPILImage()(image_tensor.squeeze(0).cpu())
    attacked_image.save(image_path)
    return call_model(image_path, prompt)
