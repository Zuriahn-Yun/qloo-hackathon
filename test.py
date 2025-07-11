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

import requests
import os

# First, search for artists to get valid URNs
search_url = "https://hackathon.api.qloo.com/v2/insights/?filter.type=urn:entity:movie&filter.tags=urn:tag:genre:media:comedy&filter.release_year.min=2022"

headers = {
    "accept": "application/json",
    "X-Api-Key": os.getenv("QLOO_API_KEY")
}

search_response = requests.get(search_url, headers=headers)
print("Search results:")
print(search_response.text)

# Then use a valid URN from the search results in your insights query