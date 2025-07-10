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
        "Content-Type": "application/json"
        }

    def get_correlations(self, entity_type, name):
        url = f"{self.base_url}/{entity_type}/correlations"
        payload = {
            "entity_type": entity_type,
            "name": str(name)
        }

        print(f"Calling: {url}")
        response = requests.post(url, headers=self.headers, json=payload)

        if response.status_code == 200:
            data = response.json()
            print("\nTop Correlations:\n")
            for item in data.get("correlations", [])[:10]:
                print(f"- {item['name']} ({item['entity_type']})")
        else:
            print(f"\nError {response.status_code}: {response.text}")

        return response
    
llama_api = llama()
#llama_api.prompt()       

qloo_api = qloo()
qloo_api.get_correlations("restaurants","starbucks")