from flask import Flask, request, jsonify, session
from flask_cors import CORS
import json
from agent import generate_report
from dotenv import load_dotenv
import os
import traceback
import threading
import uuid
# from llama_api_client import LlamaAPIClient # Assuming this is not used for this example

load_dotenv()

app = Flask(__name__)

# The CORS origin has been updated to support a frontend deployed on GitHub Pages.
# You MUST replace the placeholder URL with your actual GitHub Pages URL.
# The `origins` list can also contain multiple URLs, for example:
# origins=['https://your-username.github.io/your-repo-name/', 'http://127.0.0.1:5500']
CORS(app, origins=['*', 'https://qloo-hackathon-chi.vercel.app'], supports_credentials=True)

app.secret_key = os.environ.get('SECRET_KEY')

app.config.update(
    SESSION_COOKIE_SAMESITE="None",
    SESSION_COOKIE_SECURE=True
)

# A simple in-memory store for reports and their status.
# This will work correctly only if WEB_CONCURRENCY is set to 1.
report_store = {}

def generate_report_background(report_id, company_name, sales_data, user_query, timeframe):
    """
    A function to be run in a background thread to generate the report.
    It updates the global report_store with the result or an error message.
    """
    try:
        # Set the status to 'generating' so the frontend can poll.
        report_store[report_id] = {"status": "generating"}
        
        # This is the long-running call that would previously time out.
        report = generate_report(company_name, sales_data, user_query, timeframe)
        
        if report:
            report_store[report_id] = {"status": "completed", "report_text": report}
        else:
            report_store[report_id] = {"status": "error", "error": "Report not found"}
    except Exception as e:
        print(f"Error in background report generation: {e}")
        traceback.print_exc()
        report_store[report_id] = {"status": "error", "error": f"An error occurred: {str(e)}"}

@app.route('/submit_report_data', methods=['POST'])
def submit_report_data():
    """
    Receives user input via a POST request, saves it to the session,
    and starts a background task to generate the report.
    """
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    company_name = data.get('company')
    sales_data = data.get('sales_data')
    user_query = data.get('user_query')
    timeframe = data.get('timeframe')

    if not all([company_name, sales_data, user_query, timeframe]):
        return jsonify({"error": "Missing one or more required fields"}), 400

    # Assign a unique report ID to this session and store the data
    report_id = str(uuid.uuid4())
    session['report_id'] = report_id
    
    print("POST request received. Starting background report generation...")

    # Start the background task to generate the report.
    thread_args = (report_id, company_name, sales_data, user_query, timeframe)
    report_thread = threading.Thread(target=generate_report_background, args=thread_args)
    report_thread.daemon = True
    report_thread.start()

    # Immediately return a response to the client.
    return jsonify({"message": "Data submitted. Report generation started.", "report_id": report_id}), 200

@app.route('/get_report', methods=['GET'])
def get_report_json():
    """
    Retrieves the report from the in-memory store.
    This endpoint will be polled by the frontend to check the status of the report.
    """
    report_id = session.get('report_id')

    # If a report_id is not in the session, the user hasn't submitted data yet.
    if not report_id:
        return jsonify({"status": "error", "error": "No report has been requested yet."}), 400

    # Check the status of the report in the store.
    report_status = report_store.get(report_id)

    # If the report is still generating, tell the frontend to wait.
    if report_status and report_status['status'] == "generating":
        return jsonify({"status": "generating"}), 202 # 202 Accepted status for pending tasks
    
    # If the report is complete, return it.
    if report_status and report_status['status'] == "completed":
        # The report is completed, so we can clean up the store to prevent memory leaks.
        report_data = report_store.pop(report_id, None)
        return jsonify({"status": "completed", "report_text": report_data['report_text']}), 200

    # If an error occurred, return the error message.
    if report_status and report_status['status'] == "error":
        error_data = report_store.pop(report_id, None)
        return jsonify({"status": "error", "error": error_data['error']}), 500

    # If the report_id is in the session but not in the store, something went wrong.
    return jsonify({"status": "error", "error": "Report not found or generation failed."}), 404

# if __name__ == '__main__':
#     app.run(debug=True, host='127.0.0.1', port=5000)
