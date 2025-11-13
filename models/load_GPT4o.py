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
from torchvision import transforms
import random

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

def call_model_tensor(image_tensor, prompt):
    image_path = "temp_image.jpg"
    from PIL import Image
    import numpy as np
    attacked_image = transforms.ToPILImage()(image_tensor.squeeze(0).cpu())
    attacked_image.save(image_path)

    try:
        response = openai.chat.completions.create(
            model="gpt-4o-2024-11-20",  # or "gpt-4o" if you're using GPT-4o
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
        return "None"

def call_model(image_path, prompt):
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-2024-11-20",  # or "gpt-4o" if you're using GPT-4o
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
        return "None"