import base64
import os
import requests
import json
from bs4 import BeautifulSoup

def image_to_base64(image_path):
  with open(image_path, "rb") as img:
    return base64.b64encode(img.read()).decode('utf-8')

def extract_text_from_json(response):
	stringy = response.json()
 
	text = stringy['completion_message']
	content = text['content']
 
	final = BeautifulSoup(content['text'],'html.parser').get_text
 
	print(final)
	return final

# Read an image from the directory where this script is running
base64_image = image_to_base64("fridge.jpg")

response = requests.post(
	url="https://api.llama.com/v1/chat/completions", 
	headers={
		"Content-Type": "application/json",
	    "Authorization": f"Bearer {os.getenv('LLAMA_API_KEY')}"
	},
	json={
		"model": "Llama-4-Maverick-17B-128E-Instruct-FP8",
		"messages": [
			{
				"role": "user",
				"content": [
					{
                        "type": "text",
                        "text": "List every item in the image and its amount.",
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        },
                    },
				],
			},
		]
	}
)

extract_text_from_json(response)

