import os 
from llama_api_client import LlamaAPIClient
import requests  
import json

def basic_insights():
    # First, search for artists to get valid URNs
    search_url = "https://hackathon.api.qloo.com/v2/insights/?filter.type=urn:entity:movie&filter.tags=urn:tag:genre:media:comedy&filter.release_year.min=2025"

    headers = {
        "accept": "application/json",
        "X-Api-Key": os.getenv("QLOO_API_KEY")
    }

    search_response = requests.get(search_url, headers=headers)
    ## Pretty Print in JSON format 
    data = search_response.json()
    json_format = json.dumps(data,indent=2)
    return json_format
    
def demographics():
    # First, search for artists to get valid URNs
    search_url = "https://hackathon.api.qloo.com/v2/insights?filter.type=urn:demographics&signal.interests.tags=urn:tag:genre:media:action&signal.interests.entities=B8BEE72B-B321-481F-B81A-A44881D094D6"

    headers = {
        "accept": "application/json",
        "X-Api-Key": os.getenv("QLOO_API_KEY")
    }

    search_response = requests.get(search_url, headers=headers)
    data = search_response.json()
    json_format = json.dumps(data,indent=2)
    return json_format

def heatmaps():
    search_url = "https://hackathon.api.qloo.com/v2/insights/?filter.type=urn:heatmap&filter.location.query=NYC&signal.interests.tags=urn:tag:genre:media:non_fiction"

    headers = {
        "accept": "application/json",
        "X-Api-Key": os.getenv("QLOO_API_KEY")
    }

    search_response = requests.get(search_url, headers=headers)
    data = search_response.json()
    json_format = json.dumps(data,indent=2)
    return json_format
    
def location_insights():
    search_url = "https://hackathon.api.qloo.com/v2/insights/?filter.type=urn:entity:movie&signal.location.query=Lower%20East%20Side"

    headers = {
        "accept": "application/json",
        "X-Api-Key": os.getenv("QLOO_API_KEY")
    }

    search_response = requests.get(search_url, headers=headers)
    ## Pretty Print in JSON format 
    data = search_response.json()
    json_format = json.dumps(data,indent=2)
    return json_format

def taste_analysis():
    search_url = "https://hackathon.api.qloo.com/v2/insights?filter.type=urn%3Atag&filter.tag.types=urn%3Atag%3Akeyword%3Amedia&filter.parents.types=urn%3Aentity%3Amovie%2C%20urn%3Aentity%3Atv_show"

    headers = {
        "accept": "application/json",
        "X-Api-Key": os.getenv("QLOO_API_KEY")
    }

    search_response = requests.get(search_url, headers=headers)
    ## Pretty Print in JSON format 
    data = search_response.json()
    json_format = json.dumps(data,indent=2)
    return json_format
    
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
        basic = basic_insights()
        demo = demographics()
        mapp = heatmaps()
        location = location_insights()
        taste = taste_analysis()
        
        prompt = (
        "I am going to give you output from a QLOO API. "
        "If this were marketing data, how useful is this to you, and how could you use it to increase revenue and sales?\n\n"
        "Basic Insights:\n" + basic 
        # "\n\nDemographics:\n" + demo +
        # "\n\nHeatmaps:\n" + mapp +
        # "\n\nLocation Insights:\n" + location +
        # "\n\nTaste Analysis:\n" + taste
        )
        ## LLAMA can only really look at one of these at a time, more than that does not function
        response = self.client.chat.completions.create(
                model="Llama-4-Maverick-17B-128E-Instruct-FP8",
                    messages=[
                        {"role": "user", "content": prompt},
                    ],
                )
        print(response)
        return response
    
        
llama_api = llama()
llama_api.test()    