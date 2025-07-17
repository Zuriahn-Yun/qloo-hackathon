"""
    location_analysis -> retrieve QLOO data about a location
    brand_analysis -> retrieve QLOO data about a brand
    extract_online_image_data -> uses LLAMA for image analysis  
    
"""

tool_descriptions = [
    {
        "name": "brand_analysis",
        "description": "Searches local files for a given keyword.",
        "parameters": {
            "type": "object",
            "properties": {
                "keyword": {
                    "type": "string",
                    "description": "The keyword to search for",
                }
            },
            "required": ["keyword"]
        }
    },
    {
        "name": "location_analysis",
        "description": "Evaluates a mathematical expression.",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "A mathematical expression to evaluate",
                }
            },
            "required": ["expression"]
        }
    },
    {
        "name": "extract_online_image_data",
        "description": "Evaluates a mathematical expression.",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "A mathematical expression to evaluate",
                }
            },
            "required": ["expression"]
        }
    },
]
