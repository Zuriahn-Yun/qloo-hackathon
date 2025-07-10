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
        return response
        print(response)
        
class qloo:
    def __init__(self):
        
        self.base_url = os.getenv("QLOO_URL")
        
        self.headers = {
        "x-api-key": os.getenv("QLOO_API_KEY"),
        "accept": "application/json"
        }
        

    def test(self):
        # Try with a specific entity ID instead of just type
        url = f"{self.base_url}/v2/insights?filter.id=urn%3Aentity%3Aartist%3Ataylor-swift&feature.explainability=false"
        
        response = requests.get(url, headers=self.headers)
        print(f"Status Code: {response.status_code}")
        print(response.text)
    
#llama_api = llama()
#llama_api.prompt()       

qloo_api = qloo()
qloo_api.test()