#   https://docs.qloo.com/reference/parameters
#   https://docs.qloo.com/reference/taste-analysis
#   https://docs.qloo.com/reference/available-parameters-by-entity-type#brand

import os
import requests
import json
from llama import llama

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
    json_format = json.dumps(data,indent=2)
    #print(json_format)
    return json_format

def location_analysis(location):
    name = str(location).lower()
    split = name.split(" ")
    search_url = "https://hackathon.api.qloo.com/v2/insights?filter.type=urn%3Aentity%3Aplace&bias.trends=high&feature.explainability=false&filter.geocode.admin1_region=NY&filter.location.query=new%20york&filter.location.radius=15000"
    
    
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
    

def main():
    test = "lost angeles"
    split = test.split(" ")
    res = ""
    for i in range(len(split)):
        if i == len(split) - 1:
            res = res + split[i]
        else:
            res = res + split[i] + "%20"        
    print(res)
    
if __name__ == "__main__":
    main()



