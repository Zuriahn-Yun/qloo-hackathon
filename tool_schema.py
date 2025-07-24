"""
    location_analysis -> retrieve QLOO data about a location
    brand_analysis -> retrieve QLOO data about a brand
    extract_online_image_data -> uses LLAMA for image analysis  
    
"""

tool_descriptions = [
    {
        "name": "brand_analysis",
        "description": "RETRIEVES INSIGHT FROM THE NAME OF A BRAND using Qloo API",
        "parameters": {
            "type": "object",
            "properties": {
                "brand": {  # Fixed: was "brand_name" in description but "brand" in required
                    "type": "string",
                    "description": "The NAME OF THE BRAND to analyze",
                }
            },
            "required": ["brand"]
        }
    },
    {
        "name": "location_analysis", 
        "description": "RETRIEVES ANALYTICS REGARDING A LOCATION using Qloo API",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The name of the location to analyze",
                }
            },
            "required": ["location"]
        }
    },
    {
        "name": "extract_online_image_data",
        "description": "Evaluates an image for marketing analysis using Llama vision",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "A PUBLIC URL of an image to analyze",
                }
            },
            "required": ["url"]
        }
    },
]