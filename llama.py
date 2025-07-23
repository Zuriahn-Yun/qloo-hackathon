import os 
from llama_api_client import LlamaAPIClient
import requests  
import json
from dotenv import load_dotenv
load_dotenv()
    
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
        return response
        
    def test(self):
                
        prompt = (
        "TEST"
        )
        ## LLAMA can only really look at one of these at a time, more than that does not function        
        response = self.client.chat.completions.create(
            messages=[{"role": "user","content":prompt}
            ],
            model="Llama-4-Maverick-17B-128E-Instruct-FP8",
            temperature=0.6,
            max_completion_tokens=4096,
            repetition_penalty=1,
        )
        
        # for chunk in response:
        #     print(chunk)
        print(response)
        return response
    
    """ Get Brand Insights and Retrieve Llama output """
    def brand_test(self,brand_data):
        
        prompt = (
        "I am going to give you output for a BRAND, I want you to analyze it and retrieve all the most important insights from the data. RETURN THE MOST IMPORTANT ASPECTS AND RETAIN ALL THE IMPORTANT INFO IN A WELL ORGANIZED RESPONSE KEPT TO 300 WORDS. \n "
        "BRAND Insights:\n" + brand_data 
        )  
        response = self.client.chat.completions.create(
            
            messages=[{"role": "user","content":prompt}
            ],
            model="Llama-4-Maverick-17B-128E-Instruct-FP8",
        )
        print(response.completion_message.content.text)
        return response
    
def main():
    llama_api = llama()
    llama_api.brand_test("nutella")
    
if __name__ == "__main__":
    main()