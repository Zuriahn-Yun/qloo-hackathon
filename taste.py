#   https://docs.qloo.com/reference/parameters
#   https://docs.qloo.com/reference/taste-analysis
# https://docs.qloo.com/reference/available-parameters-by-entity-type#brand

import os
import requests
import json

def taste_analysis():
    search_url = "https://hackathon.api.qloo.com/v2/insights?filter.type=nutella%3Atag&filter.tag.types=urn%3Atag%3Akeyword%3Amedia&filter.parents.types=urn%3Aentity%3Amovie%2C%20urn%3Aentity%3Atv_show"

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

taste_analysis()

