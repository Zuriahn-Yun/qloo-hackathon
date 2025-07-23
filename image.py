import base64
import os
import requests
import json
from bs4 import BeautifulSoup
from dotenv import load_dotenv
load_dotenv()

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

def extract_online_image_data(url):
    from llama_api_client import LlamaAPIClient
    client = LlamaAPIClient()
    
    url = str(url)
    
    response = client.chat.completions.create(
    model="Llama-4-Maverick-17B-128E-Instruct-FP8",
	messages=[
        {
            "role": "user",
            "content": [
                	{
                    "type": "text",
                    "text": "DESCRIBE THIS IMAGE FOR MARKET ANALYSIS",
                	},
                	{
                    "type": "image_url",
                    "image_url": {
                        "url": url,
                    	},
                	},
				]
			}
		]
	)
    
    return response.completion_message.content.text

def extract_local_image(url):
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

	return extract_text_from_json(response)

def main():
    extract_online_image_data("https://images.qloo.com/i/3BCAD204-8191-4A9D-A403-6EAB344A98DE-0J2q58-420x-outside.jpg")
    
if __name__ == "__main__":
    main()
