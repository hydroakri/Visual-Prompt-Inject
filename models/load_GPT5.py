import argparse
import json
import os
import time
import base64
import re
from pathlib import Path
from mimetypes import guess_type
import logging
from tqdm import tqdm
import openai
import random
from openai import OpenAI
os.environ["OPENAI_API_KEY"] =""
def local_image_to_data_url(image_path):
    # Guess the MIME type of the image based on the file extension
    mime_type, _ = guess_type(image_path)
    if mime_type is None:
        mime_type = 'application/octet-stream'  # Default MIME type if none is found

    # Read and encode the image file
    with open(image_path, "rb") as image_file:
        base64_encoded_data = base64.b64encode(image_file.read()).decode('utf-8')

    # Construct the data URL
    return base64_encoded_data


client = OpenAI()
def call_model(image_path, prompt):
    try:
        data_url = f"data:image/jpeg;base64,{local_image_to_data_url(image_path)}"

        resp = client.responses.create(
            model="gpt-5",  # 或 "gpt-4o"（同为 Responses API）
            input=[{
                "role": "system",
                "content": [
                    {"type": "input_text","text": "You are a helpful assistant that generates visual editing programs from image and instruction."}
                ]
            },{
                "role": "user",
                "content": [
                    {"type": "input_text", "text": prompt},
                    {"type": "input_image", "image_url": data_url}
                ]
            }],
            max_output_tokens=1024,              # Responses API 用这个字段（不是 max_completion_tokens）
            reasoning={"effort": "minimal"},     # 降低“推理令牌”消耗

        )

        # --- 取文本输出（Responses API 推荐写法） ---
        prog = (resp.output_text or "").strip()   # SDK 提供的便捷属性
        prob = None
        return prog, prob

    except Exception as e:
        print(f"Error calling model: {e}")
        return "None"
