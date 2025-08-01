from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from llama_api_client import LlamaAPIClient
import json
import datetime
import logging

# Import tools and Schema
from tools import brand_analysis, location_analysis, extract_online_image_data
from tool_schema import tool_descriptions

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

class MarketingReportAgent:
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
        
        # Data storage for comprehensive reports
        self.collected_data = {
            "brands": {},
            "locations": {},
            "images": {},
            "sales_data": {},
            "analysis_metadata": {
                "timestamp": datetime.datetime.now().isoformat(),
                "tools_used": []
            }
        }
    
    def add_sales_data(self, brand_name, sales_data, period="weekly"):
        """Add sales data for a brand to enhance report analysis"""
        self.collected_data["sales_data"][brand_name] = {
            "period": period,
            "data_text": json.dumps(sales_data, indent=2) if isinstance(sales_data, (dict, list)) else str(sales_data),
            "timestamp": datetime.datetime.now().isoformat()
        }
    
    def execute_tool_and_store(self, tool_name, **kwargs):
        """Execute a tool and store all results for final report"""
        if tool_name not in self.tools:
            return {"error": f"Tool '{tool_name}' not found"}
        
        try:
            # Execute the tool
            result = self.tools[tool_name](**kwargs)
            
            # Store the raw data as text based on tool type
            if tool_name == "brand_analysis":
                brand_name = kwargs.get("brand", "unknown")
                data_text = json.dumps(result, indent=2) if isinstance(result, (dict, list)) else str(result)
                self.collected_data["brands"][brand_name] = {
                    "data_text": data_text,
                    "analysis_timestamp": datetime.datetime.now().isoformat()
                }
            
            elif tool_name == "location_analysis":
                location_name = kwargs.get("location", "unknown")
                data_text = json.dumps(result, indent=2) if isinstance(result, (dict, list)) else str(result)
                self.collected_data["locations"][location_name] = {
                    "data_text": data_text,
                    "analysis_timestamp": datetime.datetime.now().isoformat()
                }
            
            elif tool_name == "extract_online_image_data":
                image_url = kwargs.get("url", "unknown")
                data_text = str(result)
                self.collected_data["images"][image_url] = {
                    "data_text": data_text,
                    "analysis_timestamp": datetime.datetime.now().isoformat()
                }
            
            # Track metadata
            self.collected_data["analysis_metadata"]["tools_used"].append({
                "tool": tool_name,
                "timestamp": datetime.datetime.now().isoformat()
            })
            
            return {"success": True, "result": result}
            
        except Exception as e:
            logger.error(f"Tool execution failed: {str(e)}")
            return {"error": f"Tool execution failed: {str(e)}"}
    
    def parse_tool_calls(self, llama_response):
        """Parse tool calls from Llama response"""
        response_text = llama_response.completion_message.content.text
        
        import re
        tool_pattern = r'TOOL_CALL:\s*(\w+)\((.*?)\)'
        matches = re.findall(tool_pattern, response_text)
        
        tool_calls = []
        for match in matches:
            tool_name = match[0]
            params_str = match[1]
            
            params = {}
            if params_str:
                param_pairs = params_str.split(',')
                for pair in param_pairs:
                    if '=' in pair:
                        key, value = pair.split('=', 1)
                        key = key.strip().strip('"\'')
                        value = value.strip().strip('"\'')
                        params[key] = value
            
            tool_calls.append({
                "tool_name": tool_name,
                "parameters": params
            })
        
        return tool_calls
    
    def generate_comprehensive_report(self, user_query):
        """Main method that processes query, gathers data, and outputs comprehensive report"""
        
        # System prompt for tool planning
        planning_prompt = f"""
You are a marketing analysis agent. Your job is to determine what tools to use to gather comprehensive data for a marketing report.

Available tools:
{json.dumps(self.tool_descriptions, indent=2)}

User Query: {user_query}

Based on this query, determine what tools you need to call to gather comprehensive marketing data. 
Use this format for tool calls:
TOOL_CALL: tool_name(param="value")

You can call multiple tools. Be thorough - gather all relevant data for brands, locations, and images mentioned.
"""

        # Get tool planning response
        planning_response = self.llama_client.chat.completions.create(
            model="Llama-4-Maverick-17B-128E-Instruct-FP8",
            messages=[{"role": "user", "content": planning_prompt}],
            temperature=0.3,
            max_completion_tokens=800
        )
        
        # Execute all planned tool calls
        tool_calls = self.parse_tool_calls(planning_response)
        executed_tools = []
        
        for tool_call in tool_calls:
            result = self.execute_tool_and_store(
                tool_call["tool_name"], 
                **tool_call["parameters"]
            )
            executed_tools.append({
                "tool": tool_call["tool_name"],
                "parameters": tool_call["parameters"],
                "result": result
            })
        
        # Generate comprehensive report
        report = self._generate_final_report(executed_tools)
        
        return report
    
    def _generate_final_report(self, executed_tools):
        """Generate comprehensive marketing report with all collected data"""
        
        # Create comprehensive report prompt with all text data including sales data
        report_prompt = f"""
You are creating a comprehensive marketing and sales analysis report for business executives. This report will be printed and placed on someone's desk - it must be in PLAIN TEXT format only, no markdown, no formatting symbols, just readable business prose.

BRAND DATA COLLECTED:
{json.dumps({k: v['data_text'] for k, v in self.collected_data['brands'].items()}, indent=2)}

LOCATION DATA COLLECTED:
{json.dumps({k: v['data_text'] for k, v in self.collected_data['locations'].items()}, indent=2)}

IMAGE ANALYSIS DATA COLLECTED:
{json.dumps({k: v['data_text'] for k, v in self.collected_data['images'].items()}, indent=2)}

SALES DATA COLLECTED:
{json.dumps({k: v['data_text'] for k, v in self.collected_data['sales_data'].items()}, indent=2)}

Create a detailed business report in PLAIN TEXT format that reads like a professional document. Structure it as follows:

EXECUTIVE SUMMARY
Write a clear overview of key findings, critical insights, and major opportunities. Include specific metrics and data points from both market research and sales performance.

BRAND PERFORMANCE ANALYSIS
For each brand analyzed, provide complete analysis including:
- Detailed brand profile with ALL data points and metrics from market research
- Current sales performance with specific numbers, increases, and decreases
- Market position and competitive standing based on both sales and market data
- Consumer sentiment analysis with specific feedback and how it correlates to sales
- Sales trend analysis showing week-over-week or month-over-month changes
- Target demographic breakdown with purchasing behavior specifics
- Brand strengths, weaknesses, and market gaps affecting sales
- Revenue impact analysis with concrete figures
- Product line performance breakdown showing top and bottom performers

MARKET LOCATION ANALYSIS
For each location analyzed, provide:
- Complete demographic and economic profile affecting sales potential
- Consumer behavior patterns and actual purchasing trends from sales data
- Local competition landscape and market share impact on performance
- Seasonal buying patterns with sales data correlation
- Regional preferences and cultural factors driving sales variations
- Economic indicators affecting purchasing power and sales volume
- Location-specific opportunities for sales growth

SALES PERFORMANCE DEEP DIVE
Analyze current sales data in detail:
- Products showing strong sales growth and reasons why
- Products with declining sales and root cause analysis
- Inventory turnover rates and stock optimization needs
- Price point analysis and revenue per unit trends
- Customer acquisition costs versus lifetime value
- Sales channel performance comparison
- Seasonal sales patterns and forecasting implications

SALES OPTIMIZATION RECOMMENDATIONS
Based on combined market and sales data, provide specific guidance on:
- Products to immediately increase inventory and marketing spend for based on sales momentum
- Underperforming products requiring urgent strategy changes or discontinuation
- Pricing optimization opportunities to maximize revenue
- Inventory management recommendations to reduce carrying costs
- Sales channel optimization to improve conversion rates
- Customer acquisition strategies with projected ROI
- Revenue growth initiatives with specific targets and timelines

IMMEDIATE ACTION ITEMS
List specific, actionable steps with:
- Timeline for implementation within the next 30, 60, and 90 days
- Budget allocation recommendations with expected returns
- Resource requirements and staffing needs
- Expected ROI and success metrics for each action
- Risk assessment and mitigation strategies
- Performance monitoring and adjustment protocols

STRATEGIC NEXT STEPS
Provide detailed long-term recommendations including:
- Market expansion opportunities based on sales data patterns
- Product development priorities driven by sales performance gaps
- Brand positioning adjustments to improve sales conversion
- Investment allocation strategies for maximum sales impact
- Partnership and collaboration opportunities to boost sales
- Technology and infrastructure needs to support sales growth
- Long-term market positioning to sustain sales leadership

CRITICAL: Include ALL specific numbers, percentages, metrics, demographic data, sales figures, and insights from the collected data. Do not use any markdown formatting, bullet points, or special symbols. Write in clear business prose as if this were a formal business document. Make it comprehensive enough that executives can make informed decisions about sales strategy, inventory management, marketing budget allocation, and product line decisions. Focus heavily on actionable insights that will directly impact sales performance and revenue growth.
"""

        # Generate the comprehensive plain text report
        final_response = self.llama_client.chat.completions.create(
            model="Llama-4-Maverick-17B-128E-Instruct-FP8",
            messages=[{"role": "user", "content": report_prompt}],
            temperature=0.4,
            max_completion_tokens=4096
        )
        
        return final_response.completion_message.content.text

# API Routes

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "timestamp": datetime.datetime.now().isoformat()})

@app.route('/api/generate-report', methods=['POST'])
def generate_report():
    """
    Generate a comprehensive marketing report
    Expected JSON payload:
    {
        "brand": "Nike",
        "location": "Los Angeles",
        "item_type": "running shoes",
        "sales_change": "increase",
        "sales_percentage": 15,
        "additional_context": "Optional additional context"
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['brand', 'location', 'item_type', 'sales_change']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({
                "error": "Missing required fields",
                "missing_fields": missing_fields
            }), 400
        
        # Extract data from request
        brand = data.get('brand')
        location = data.get('location')
        item_type = data.get('item_type')
        sales_change = data.get('sales_change')  # 'increase' or 'decrease'
        sales_percentage = data.get('sales_percentage', 0)
        additional_context = data.get('additional_context', '')
        
        # Create agent instance
        agent = MarketingReportAgent()
        
        # Create sales data based on input
        sales_data = {
            "item_type": item_type,
            "trend": sales_change,
            "percentage_change": f"{'+' if sales_change == 'increase' else '-'}{sales_percentage}%",
            "context": additional_context,
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        # Add sales data to agent
        agent.add_sales_data(brand.lower(), sales_data)
        
        # Generate query for the agent
        query = f"Analyze {brand}'s brand performance for {item_type} in {location} market. " \
                f"Sales have shown a {sales_change} of {sales_percentage}%. {additional_context}".strip()
        
        # Generate comprehensive report
        report = agent.generate_comprehensive_report(query)
        
        return jsonify({
            "success": True,
            "report": report,
            "metadata": {
                "brand": brand,
                "location": location,
                "item_type": item_type,
                "sales_change": sales_change,
                "sales_percentage": sales_percentage,
                "generated_at": datetime.datetime.now().isoformat()
            }
        })
        
    except Exception as e:
        logger.error(f"Error generating report: {str(e)}")
        return jsonify({
            "error": "Failed to generate report",
            "message": str(e)
        }), 500

@app.route('/api/quick-analysis', methods=['POST'])
def quick_analysis():
    """
    Quick brand analysis without full report generation
    Expected JSON payload:
    {
        "brand": "Nike",
        "analysis_type": "brand" | "location" | "image",
        "target": "brand_name" | "location_name" | "image_url"
    }
    """
    try:
        data = request.get_json()
        
        if 'brand' not in data or 'analysis_type' not in data or 'target' not in data:
            return jsonify({
                "error": "Missing required fields: brand, analysis_type, target"
            }), 400
        
        analysis_type = data.get('analysis_type')
        target = data.get('target')
        
        # Create agent instance
        agent = MarketingReportAgent()
        
        # Execute specific tool based on analysis type
        if analysis_type == 'brand':
            result = agent.execute_tool_and_store('brand_analysis', brand=target)
        elif analysis_type == 'location':
            result = agent.execute_tool_and_store('location_analysis', location=target)
        elif analysis_type == 'image':
            result = agent.execute_tool_and_store('extract_online_image_data', url=target)
        else:
            return jsonify({
                "error": "Invalid analysis_type. Must be 'brand', 'location', or 'image'"
            }), 400
        
        return jsonify({
            "success": True,
            "analysis_type": analysis_type,
            "target": target,
            "result": result,
            "timestamp": datetime.datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in quick analysis: {str(e)}")
        return jsonify({
            "error": "Failed to perform analysis",
            "message": str(e)
        }), 500

@app.route('/api/brands', methods=['GET'])
def get_supported_brands():
    """Get list of supported brands for analysis"""
    # This could be dynamic based on your tools' capabilities
    supported_brands = [
        "Nike", "Adidas", "Apple", "Samsung", "Coca-Cola", "Pepsi", 
        "McDonald's", "Starbucks", "Amazon", "Google", "Facebook", "Tesla"
    ]
    
    return jsonify({
        "supported_brands": supported_brands,
        "total_count": len(supported_brands)
    })

@app.route('/api/locations', methods=['GET'])
def get_supported_locations():
    """Get list of supported locations for analysis"""
    supported_locations = [
        "New York", "Los Angeles", "Chicago", "Houston", "Phoenix",
        "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose",
        "Austin", "Jacksonville", "Fort Worth", "Columbus", "Charlotte"
    ]
    
    return jsonify({
        "supported_locations": supported_locations,
        "total_count": len(supported_locations)
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    # Use environment variables for configuration
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    app.run(host='0.0.0.0', port=port, debug=debug)