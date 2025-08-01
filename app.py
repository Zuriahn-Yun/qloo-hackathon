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
            as_attachment=False, # True: sends a download link. False: Displays content in browser
            download_name="marketing_report",
            mimetype='text/plain'
        )
    return jsonify({"error": "File not found"}), 404


# API ideas

# user submits query for all company reports -> get request for all reports
# 
# add sales data is a post request into backend DB


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
    
    