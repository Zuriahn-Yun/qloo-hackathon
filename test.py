import os 
from llama_api_client import LlamaAPIClient
import requests

class llama():
    def __init__(self):
        self.client = LlamaAPIClient(
            api_key=os.getenv("LLAMA_API_KEY"),
            base_url=os.getenv("base_url"),
            )
    def prompt(self):
        response = self.client.chat.completions.create(
                model="Llama-4-Maverick-17B-128E-Instruct-FP8",
                    messages=[
                        {"role": "user", "content": "How can i best integrate you with QLOO"},
                    ],
                )
        print(response)
        
llama_api = llama()
llama_api.prompt()       

class qloo:
    def __init__(self):
        print("here")
        url = os.getenv("QLOO_URL")
        key = os.getenv("QLOO_API_KEY")