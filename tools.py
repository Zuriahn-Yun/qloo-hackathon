#   https://docs.qloo.com/reference/parameters
#   https://docs.qloo.com/reference/taste-analysis
#   https://docs.qloo.com/reference/available-parameters-by-entity-type#brand

import os
import requests
import json
from llama import llama
from dotenv import load_dotenv
load_dotenv()

### INSIGHTS PAGE https://docs.qloo.com/reference/insights-api-deep-dive 


# Searching for brands
def brand_analysis(brand):
    name = str(brand).lower()
    search_url = "https://hackathon.api.qloo.com/search?query=" + brand + "&filter.radius=10&operator.filter.tags=union&page=1&sort_by=match"
    
    headers = {
        "accept": "application/json",
        "X-Api-Key": os.getenv("QLOO_API_KEY")
    }

    search_response = requests.get(search_url, headers=headers)
    ## Pretty Print in JSON format 
    data = search_response.json()
    """ FOR PRETTY PRINT AND JSON FORMAT, OTHERWISE RETURN DATA """
    json_format = json.dumps(data,indent=2)
    #print(json_format)
    return data

def location_analysis(location):
   
    def parse(location):
        split = location.split(" ")
        res = ""
        for i in range(len(split)):
            if i == len(split) - 1:
                res = res + split[i]
            else:
                res = res + split[i] + "%20"
        return res
    
    res = parse(location)
    
            
    search_url = "https://hackathon.api.qloo.com/v2/insights?filter.type=urn%3Aentity%3Aplace&bias.trends=high&feature.explainability=false&filter.location.query=" + res + "&filter.location.radius=15000"
    
    
    headers = {
        "accept": "application/json",
        "X-Api-Key": os.getenv("QLOO_API_KEY")
    }

    search_response = requests.get(search_url, headers=headers)
    
    ## Pretty Print in JSON format 
    data = search_response.json()
    json_format = json.dumps(data,indent=2)
    print(json_format)
    return json_format

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
def main():
    
    """
    location_analysis -> retrieve QLOO data about a location
    brand_analysis -> retrieve QLOO data about a brand
    extract_online_image_data -> uses LLAMA for image analysis  
    
    """
    llama_api = llama()
    
    brand_output = brand_analysis("nutella")
    print(llama_api.brand_test(brand_output))
    
if __name__ == "__main__":
    main()



