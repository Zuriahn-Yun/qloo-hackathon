#   https://docs.qloo.com/reference/parameters
#   https://docs.qloo.com/reference/taste-analysis
#   https://docs.qloo.com/reference/available-parameters-by-entity-type#brand

import os
import requests
import json
from llama import llama

# This si for searching for brands
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

def main():
    brands = ["NUTELLA","monster","NUTELLA","PEPSI"]

    llama_api = llama()
    data = brand_analysis("nutella")

    output = llama.brand_insights(llama_api,brand_data=data)

    print(output)
    
if __name__ == "__main__":
    main()



