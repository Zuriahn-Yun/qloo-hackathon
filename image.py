import base64
import os
import requests

def image_to_base64(image_path):
  with open(image_path, "rb") as img:
    return base64.b64encode(img.read()).decode('utf-8')

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
                        "text": "List every item within the fridge.",
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
print(response.text)