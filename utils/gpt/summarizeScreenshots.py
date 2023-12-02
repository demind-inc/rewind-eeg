import openai
import requests
import base64
import json

import config

my_openai_key = config.api_key

def get_image_description(base64_image, prompt_text, followup_message=None):
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
                        "text": prompt_text
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

def parse_prompt(prompt_file):
    with open(prompt_file, 'r') as file:
        file_content = file.read()
    prompt_text = file_content.replace('\n', ' ')
    return prompt_text

def summarizeScreenshot(filepath):
    ss = config.basedir + 'utils/rewind/screenShots/' + filepath 
    base64_image = encode_image(ss)
    prompt_text = parse_prompt("prompts/prompt2.txt")
    resp = get_image_description(base64_image, prompt_text)
    with open('resp3.json', 'w') as f: 
        f.write(json.dumps(resp))
    return resp["choices"][0]["message"]["content"]

if __name__ == "__main__":
    ss = config.basedir + 'utils/rewind/screenShots/' + 'image.png' # change image file here
    base64_image = encode_image(ss)
    prompt_text = parse_prompt("prompts/prompt2.txt")
    resp = get_image_description(base64_image, prompt_text)
    with open('resp3.json', 'w') as f: 
        f.write(json.dumps(resp))
    print(resp["choices"][0]["message"]["content"])