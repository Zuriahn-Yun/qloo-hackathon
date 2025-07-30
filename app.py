from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import json
from agent import generate_report
from dotenv import load_dotenv
import os
from llama_api_client import LlamaAPIClient

load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route('/')
def test():
    return "TESTING HELLO WORLD"

@app.route('/get_report', methods=['GET'])
def get_report():
    generate_report()
    filepath='marketing_analysis_report.txt'
    if os.path.exists(filepath):
        print("success!")
        return send_file(
            filepath,
            as_attachment=False,
            download_name="marketing_report",
            mimetype='text/plain'
        )
    return jsonify({"error": "File not found"}), 404

# add sales data is a post request into backend DB


# # Register the API blueprint

# @app.route('/')
# def home():
#     return jsonify({
#         "message": "Welcome to the Event Planning API",
#         "endpoints": {
#             "process_input": "POST /process_input - Process user input for event planning"
#         }
#     })

# # predcondition: user has already selected a location, interest, time, and date
# @app.route('/handle_preferences', methods=['POST'])
# def handle_preferences():
#     data = request.json
#     if not data:
#         return jsonify({"error": "No data provided"}), 400
#     stringified_json = json.dumps(data)
#     # call agent to handle preferences
#     response = run_agent(stringified_json)
#     return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
    
    