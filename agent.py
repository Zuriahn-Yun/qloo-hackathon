from dotenv import load_dotenv
import os
from llama_api_client import LlamaAPIClient
import json

# Import tools and Schema
from tools import brand_analysis, location_analysis, extract_online_image_data
from tool_schema import tool_descriptions

load_dotenv()

class MarketingAgent:
    def __init__(self):
        self.llama_client = LlamaAPIClient(
            api_key=os.getenv("LLAMA_API_KEY"),
            base_url=os.getenv("base_url"),
        )
        
        # Register your tools
        self.tools = {
            "brand_analysis": brand_analysis,
            "location_analysis": location_analysis, 
            "extract_online_image_data": extract_online_image_data
        }
        
        self.tool_descriptions = tool_descriptions
        
def main():
    print("NO errror")
    
if __name__ == "__main__":
    main()
