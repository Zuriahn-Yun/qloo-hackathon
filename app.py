from flask import Flask, request, jsonify, session
from flask_cors import CORS
import json
from agent import generate_report
from dotenv import load_dotenv
import os
import traceback # Import the traceback module to print detailed error information

load_dotenv()

app = Flask(__name__)

# The CORS origin is now explicitly set to your local frontend's URL.
# This is a more secure and reliable configuration than a wildcard.
CORS(app, origins=['http://127.0.0.1:5500'], supports_credentials=True)

# The secret key is explicitly read from an environment variable.
# The application will fail to start if SECRET_KEY is not set.
app.secret_key = os.environ.get('SECRET_KEY')

# This is the critical change to ensure the session persists between POST and GET requests.
# The 'SameSite' attribute is set to 'None' to allow the cookie to be sent with cross-site requests.
# The 'Secure' attribute is set to True, which is required when 'SameSite' is 'None'.
app.config.update(
    SESSION_COOKIE_SAMESITE="None",
    SESSION_COOKIE_SECURE=True
)

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

    print("POST request received. Session data stored:")
    print("Company:", session.get('company'))
    print("Sales Data:", session.get('sales_data'))
    print("User Query:", session.get('user_query'))
    print("Timeframe:", session.get('timeframe'))

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

    print("GET request received. Session data retrieved:")
    print("Company:", session.get('company'))
    print("Sales Data:", session.get('sales_data'))
    print("User Query:", session.get('user_query'))
    print("Timeframe:", session.get('timeframe'))

    # Check if all data is present
    if not all([company_name, sales_data, user_query, timeframe]):
        return jsonify({"error": "Please submit all data first via POST to /submit_report_data"}), 400
    
    # Pass all the stored data as arguments to your generate_report function.
    try:
        #report = generate_report(company_name, sales_data, user_query, timeframe)
        with open("marketing_analysis_report.txt", 'r') as file:
            report = file.read()

        if report:
            return jsonify({"report_text": report}), 200
        else:
            return jsonify({"error": "Report not found"}), 404
    except Exception as e:
        # Catch any exception and return a specific error message.
        # This will prevent the 502 Bad Gateway and give us more information.
        print(f"Error in generate_report: {e}")
        traceback.print_exc()
        return jsonify({"error": f"An error occurred while generating the report: {e}"}), 500

# if __name__ == '__main__':
#     app.run(debug=True, host='127.0.0.1', port=5000)
