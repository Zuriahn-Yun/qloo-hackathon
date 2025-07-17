class Agent:
    
    
    def __init__(self):
        from llama import llama
        llama_api = llama()
        
        
    def run(self):
        print("...running")
        tools = [
            self.brand_analysis()
        ]
        
        
    """ USE QLOO API TO RETRIEVE BRAND DATA """
    def brand_analysis(self,brand):
        from tools import brand_analysis
        return brand_analysis(brand=brand)