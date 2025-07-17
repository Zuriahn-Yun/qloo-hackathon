"""
    location_analysis -> retrieve QLOO data about a location
    brand_analysis -> retrieve QLOO data about a brand
    extract_online_image_data -> uses LLAMA for image analysis  
    
"""

tool_descriptions = [
    {
        "name": "brand_analysis",
        "description": "RETRIEVES INSIGHT FROM THE NAME OF A BRAND",
        "parameters": {
            "type": "object",
            "properties": {
                "brand_name": {
                    "type": "string",
                    "description": "The NAME OF THE BRAND",
                }
            },
            "required": ["brand"]
        }
    },
    {
        "name": "location_analysis",
        "description": "RETRIEVES ANALYTICS REGARDING A LOCATION",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "the name of the location",
                }
            },
            "required": ["location"]
        }
    },
    {
        "name": "extract_online_image_data",
        "description": "Evaluates an image",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "A PUBLIC URL PROVIDED FROM location_analysis or brand_analysis",
                }
            },
            "required": ["url"]
        }
    },
]
