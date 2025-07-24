from dotenv import load_dotenv
import os
from llama_api_client import LlamaAPIClient
import json

# Import tools and Schema
from tools import brand_analysis, location_analysis, extract_online_image_data
from tool_schema import tool_descriptions
import datetime

load_dotenv()

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
        
        # Data storage for comprehensive reports - just retain all data in text format
        self.collected_data = {
            "brands": {},
            "locations": {},
            "images": {},
            "sales_data": {},  # New: for weekly/monthly sales data
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
                # Convert result to text format for storage
                data_text = json.dumps(result, indent=2) if isinstance(result, (dict, list)) else str(result)
                self.collected_data["brands"][brand_name] = {
                    "data_text": data_text,
                    "analysis_timestamp": datetime.datetime.now().isoformat()
                }
            
            elif tool_name == "location_analysis":
                location_name = kwargs.get("location", "unknown")
                # Convert result to text format for storage
                data_text = json.dumps(result, indent=2) if isinstance(result, (dict, list)) else str(result)
                self.collected_data["locations"][location_name] = {
                    "data_text": data_text,
                    "analysis_timestamp": datetime.datetime.now().isoformat()
                }
            
            elif tool_name == "extract_online_image_data":
                image_url = kwargs.get("url", "unknown")
                # Store image analysis result as text
                data_text = str(result)
                self.collected_data["images"][image_url] = {
                    "data_text": data_text,
                    "analysis_timestamp": datetime.datetime.now().isoformat()
                }
            
            # Track metadata - simplified
            self.collected_data["analysis_metadata"]["tools_used"].append({
                "tool": tool_name,
                "timestamp": datetime.datetime.now().isoformat()
            })
            
            return {"success": True, "result": result}
            
        except Exception as e:
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
        
        # Return only the plain text report
        return final_response.completion_message.content.text
    
    def get_data_about(self, entity_name):
        """Retrieve all stored data about a specific brand, location, or image"""
        results = {
            "entity": entity_name,
            "found_data": {}
        }
        
        # Check brands
        for brand_name, brand_data in self.collected_data["brands"].items():
            if entity_name.lower() in brand_name.lower():
                results["found_data"]["brand_data"] = {
                    "brand_name": brand_name,
                    "data": brand_data["data_text"]
                }
        
        # Check locations
        for location_name, location_data in self.collected_data["locations"].items():
            if entity_name.lower() in location_name.lower():
                results["found_data"]["location_data"] = {
                    "location_name": location_name,
                    "data": location_data["data_text"]
                }
        
        # Check images
        for image_url, image_data in self.collected_data["images"].items():
            if entity_name.lower() in image_url.lower():
                results["found_data"]["image_data"] = {
                    "image_url": image_url,
                    "data": image_data["data_text"]
                }
        
        return results
    
    def export_report(self, report_text, filename=None):
        """Export plain text report to file"""
        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(report_text)
            return f"Report exported to {filename}"
        return report_text

# Usage examples
def main():
    agent = MarketingReportAgent()
    
    print("=== Marketing Report Agent Demo ===\n")
    
    # Add sales data for brands
    nike_sales = {
        "weekly_sales": {
            "air_jordan": {"units": 1250, "revenue": 187500, "change": "+15%"},
            "air_max": {"units": 890, "revenue": 89000, "change": "-5%"},
            "running_shoes": {"units": 2100, "revenue": 168000, "change": "+22%"}
        },
        "trends": "Strong growth in running category, Jordan line maintaining premium pricing"
    }
    
    agent.add_sales_data("nike", nike_sales, "weekly")
    
    # Generate comprehensive plain text report
    report = agent.generate_comprehensive_report(
        "Analyze Nike's brand performance and market opportunities in Los Angeles with current sales data"
    )
    
    print("PLAIN TEXT BUSINESS REPORT:")
    print("=" * 80)
    print(report)
    print("=" * 80)
    
    # Export to file
    export_result = agent.export_report(report, "marketing_analysis_report.txt")
    print(f"\n{export_result}")
    
    # Retrieve specific brand data
    nike_data = agent.get_data_about("nike")
    print(f"\nNike Data Available: {list(nike_data['found_data'].keys())}")

if __name__ == "__main__":
    main()