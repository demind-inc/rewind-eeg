import openai
import requests
import base64

import config

my_openai_key = config.api_key

def get_image_description(base64_image, followup_message=None):
    print("Sending request to GPT-4 Vision API...")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {my_openai_key}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "What’s in this image?"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                            "detail": "low"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 1000
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    return response.json()

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

if __name__ == "__main__":
    ss = config.basedir + 'screenshots/image1.png'
    base64_image = encode_image(ss)
    resp = get_image_description(base64_image)
    print(resp)