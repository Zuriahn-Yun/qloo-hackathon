from flask import Flask, request, jsonify, session
from flask_cors import CORS
import json
from agent import generate_report
from dotenv import load_dotenv
import os
from llama_api_client import LlamaAPIClient

load_dotenv()

app = Flask(__name__)
CORS(app, origins=['http://127.0.0.1:5500'], supports_credentials=True)

app.secret_key = os.urandom(24)



@app.route('/submit_report_data', methods=['POST'])
def submit_report_data():
    """
    Receives user input via a POST request and saves all four fields to the session.
    The frontend will send a JSON payload with the required data.
    """

    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    company_name = data.get('company')
    sales_data = data.get('sales_data')
    user_query = data.get('user_query')
    timeframe = data.get('timeframe')

    
    # Validate that all required fields are present
    if not all([company_name, sales_data, user_query, timeframe]):
        return jsonify({"error": "Missing one or more required fields"}), 400

    # Store all of the user's data in the Flask session.
    session['company'] = company_name
    session['sales_data'] = sales_data
    session['user_query'] = user_query
    session['timeframe'] = timeframe

    print(session['company'])
    print(session['sales_data'])
    print(session['user_query'])
    print(session['timeframe'])

    return jsonify({"message": "Company, sales data, query, and timeframe saved successfully."}), 200


@app.route('/get_report', methods=['GET'])
def get_report_json():
    """
    Retrieves the data from the session and uses it to generate the report.
    """
    # Retrieve all required data from the session.
    company_name = session.get('company')
    sales_data = session.get('sales_data')
    user_query = session.get('user_query')
    timeframe = session.get('timeframe')

    print(session['company'])
    print(session['sales_data'])
    print(session['user_query'])
    print(session['timeframe'])

    # Check if all data is present
    if not all([company_name, sales_data, user_query, timeframe]):
        return jsonify({"error": "Please submit all data first via POST to /submit_report_data"}), 400
    
    # Pass all the stored data as arguments to your generate_report function.
    report = generate_report(company_name, sales_data, user_query, timeframe)
    
    if report:
        return jsonify({"report_text": report}), 200
    
    return jsonify({"error": "Report not found"}), 404


# API ideas

# user submits query for all company reports -> get request for all reports
# 
# add sales data is a post request into backend DB



@app.route('/docs', methods=['GET'])
def api_docs():
    """
    Serves a simple JSON documentation for the API.
    """
    docs = {
        "api_documentation": "Welcome to the Report Generator API!",
        "endpoints": {
            "/submit_report_data": {
                "method": "POST",
                "description": "Receives user input and saves it to the session. Must be called before /get_report.",
                "request_body": {
                    "company": "string (e.g., 'Acme Corp')",
                    "sales_data": "JSON object (e.g., {'2023': 150000, '2024': 180000})",
                    "user_query": "string (e.g., 'Analyze our sales performance')",
                    "timeframe": "string (e.g., 'Q1 2024')"
                },
                "response": {
                    "200 OK": {"message": "string"}
                }
            },
            "/get_report": {
                "method": "GET",
                "description": "Generates a report based on the data submitted via /submit_report_data.",
                "request_params": "None",
                "response": {
                    "200 OK": {"report_text": "string (the generated report)"},
                    "400 Bad Request": {"error": "Please submit all data first via POST to /submit_report_data"},
                    "404 Not Found": {"error": "Report not found"}
                }
            }
        }
    }
    return jsonify(docs)



    