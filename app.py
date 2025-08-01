from flask import Flask, request, jsonify, session
from flask_cors import CORS
import json
from agent import generate_report
from dotenv import load_dotenv
import os
from llama_api_client import LlamaAPIClient

load_dotenv()



app = Flask(__name__)
CORS(app)

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


@app.route('/')
def serve_frontend():
    """
    Serves the HTML frontend file when the user visits the root URL.
    """
    # This is where we'll serve the HTML content from the other immersive.
    # In a real app, you would use render_template() with a Jinja2 template.
    # For this example, we'll just return the raw HTML string.
    # IMPORTANT: Ensure your `report_generator_frontend` content is in the same directory.
    # For simplicity, I will include the HTML here in the string.
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Report Generator</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body {
            font-family: 'Inter', sans-serif;
            background-color: #1a202c;
        }
        .container {
            max-width: 800px;
        }
    </style>
</head>
<body class="bg-gray-900 text-gray-200 p-8 flex items-center justify-center min-h-screen">
    <div class="container mx-auto p-8 bg-gray-800 rounded-xl shadow-lg">
        <h1 class="text-4xl font-bold text-center mb-8 text-white">Report Generator</h1>
        
        <!-- Form for user input -->
        <form id="report-form" class="space-y-6">
            <div>
                <label for="company_name" class="block text-sm font-medium text-gray-400">Company Name</label>
                <input type="text" id="company_name" name="company" placeholder="e.g., Acme Corp" class="mt-1 block w-full px-4 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500">
            </div>
            <div>
                <label for="sales_data" class="block text-sm font-medium text-gray-400">Sales Data (JSON format)</label>
                <textarea id="sales_data" name="sales_data" rows="4" placeholder='e.g., {"2023": 150000, "2024": 180000}' class="mt-1 block w-full px-4 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"></textarea>
            </div>
            <div>
                <label for="user_query" class="block text-sm font-medium text-gray-400">Your Query</label>
                <input type="text" id="user_query" name="user_query" placeholder="e.g., Analyze our sales performance" class="mt-1 block w-full px-4 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500">
            </div>
            <div>
                <label for="timeframe" class="block text-sm font-medium text-gray-400">Timeframe</label>
                <input type="text" id="timeframe" name="timeframe" placeholder="e.g., Q1 2024" class="mt-1 block w-full px-4 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500">
            </div>

            <div class="flex items-center justify-between space-x-4 pt-4">
                <button type="submit" class="w-full px-6 py-3 text-lg font-semibold text-white bg-green-600 rounded-lg shadow-lg hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 transition duration-300">
                    Submit Data
                </button>
                <button type="button" id="get-report-btn" class="w-full px-6 py-3 text-lg font-semibold text-white bg-blue-600 rounded-lg shadow-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition duration-300">
                    Get Report
                </button>
            </div>
        </form>

        <!-- Loading indicator and status messages -->
        <div id="status-message" class="mt-8 text-center text-sm font-medium text-gray-400"></div>

        <!-- Textbox to display the report -->
        <div class="mt-8">
            <h2 class="text-2xl font-bold text-center mb-4 text-white">Generated Report</h2>
            <textarea id="report-output" rows="10" readonly class="w-full p-4 bg-gray-700 border border-gray-600 rounded-lg text-white font-mono leading-relaxed resize-none focus:outline-none focus:ring-2 focus:ring-blue-500"></textarea>
        </div>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', () => {
            const form = document.getElementById('report-form');
            const getReportBtn = document.getElementById('get-report-btn');
            const statusMessage = document.getElementById('status-message');
            const reportOutput = document.getElementById('report-output');
            const API_URL = 'http://127.0.0.1:5000';

            // Handle form submission to send data via POST
            form.addEventListener('submit', async (e) => {
                e.preventDefault();
                
                statusMessage.textContent = 'Submitting data...';
                reportOutput.value = '';

                const formData = new FormData(form);
                const data = {};
                formData.forEach((value, key) => {
                    data[key] = key === 'sales_data' ? JSON.parse(value) : value;
                });

                try {
                    const response = await fetch(`${API_URL}/submit_report_data`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(data)
                    });

                    const result = await response.json();
                    
                    if (response.ok) {
                        statusMessage.textContent = result.message;
                        statusMessage.className = 'mt-8 text-center text-sm font-medium text-green-500';
                    } else {
                        statusMessage.textContent = `Error: ${result.error}`;
                        statusMessage.className = 'mt-8 text-center text-sm font-medium text-red-500';
                    }

                } catch (error) {
                    statusMessage.textContent = 'Failed to submit data. Is the server running?';
                    statusMessage.className = 'mt-8 text-center text-sm font-medium text-red-500';
                    console.error('Error:', error);
                }
            });

            // Handle button click to get the report via GET
            getReportBtn.addEventListener('click', async () => {
                statusMessage.textContent = 'Generating report...';
                reportOutput.value = '';

                try {
                    const response = await fetch(`${API_URL}/get_report`);
                    const result = await response.json();
                    
                    if (response.ok) {
                        statusMessage.textContent = 'Report generated successfully!';
                        statusMessage.className = 'mt-8 text-center text-sm font-medium text-green-500';
                        reportOutput.value = result.report_text;
                    } else {
                        statusMessage.textContent = `Error: ${result.error}`;
                        statusMessage.className = 'mt-8 text-center text-sm font-medium text-red-500';
                        reportOutput.value = '';
                    }

                } catch (error) {
                    statusMessage.textContent = 'Failed to get report. Please submit data and try again.';
                    statusMessage.className = 'mt-8 text-center text-sm font-medium text-red-500';
                    console.error('Error:', error);
                }
            });
        });
    </script>
</body>
</html>
    """

# if __name__ == '__main__':
#     app.run(debug=True, host='127.0.0.1', port=5000)
    
    