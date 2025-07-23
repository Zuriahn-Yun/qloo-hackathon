from dotenv import load_dotenv
load_dotenv()

class Agent: 
    def __init__(self):
        from llama import llama
        from tools import brand_analysis,location_analysis,extract_online_image_data
        from tool_schema import tool_descriptions
        
        llama_api = llama()
        
        tools = {
            "brand_analysis" : brand_analysis,
            "location_analysis" : location_analysis,
            "extract_online_image_data" : extract_online_image_data,
        }
        
def main():
    while True:
        print(4)
    
if __name__ == "__main__":
    main()
