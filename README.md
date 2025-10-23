# Sales Report Generator - Hackathon Project

An AI-powered sales analytics report generator that analyzes brand performance, location insights, and sales data to provide actionable business recommendations.

## 🚀 Features

- **AI-Powered Analysis**: Uses Llama AI for intelligent report generation
- **Brand Analysis**: Gather comprehensive brand data using Qloo API
- **Location Insights**: Analyze market trends by geographic location
- **Sales Performance**: Deep dive into sales data with actionable recommendations
- **Asynchronous Processing**: Background task processing for long-running reports

## 🛠️ Tech Stack

**Backend:**
- FastAPI (Python web framework)
- Uvicorn (ASGI server)
- Llama API (AI/LLM integration)
- Qloo API (Brand and market data)

**Frontend:**
- HTML/JavaScript (Vanilla JS)
- Tailwind CSS
- Lucide Icons

## 📋 Prerequisites

Before running this application, make sure you have:

- Python 3.8 or higher
- pip (Python package manager)
- API Keys:
  - Llama API Key ([Get it here](https://www.llama.com/))
  - Qloo API Key ([Get it here](https://www.qloo.com/))

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd qloo-hackathon
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root by copying the example:

```bash
cp .env.example .env
```

Then edit `.env` and add your actual API keys:

```env
LLAMA_API_KEY=your_actual_llama_api_key
base_url=https://api.llama.com
QLOO_API_KEY=your_actual_qloo_api_key
SECRET_KEY=your_random_secret_key
PORT=8000
```

### 4. Run the backend server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Or simply:

```bash
python main.py
```

The API will be available at `http://localhost:8000`

### 5. Open the frontend

Open `index.html` in your web browser, or use a local server:

```bash
# Using Python's built-in server
python -m http.server 3000
```

Then navigate to `http://localhost:3000`

## 📚 API Documentation

Once the server is running, visit:
- **Interactive API Docs**: `http://localhost:8000/docs`
- **Alternative Docs**: `http://localhost:8000/redoc`

### Main Endpoints

#### POST `/submit_report_data`
Submit data to generate a sales report.

**Request Body:**
```json
{
  "company": "Nike",
  "sales_data": {
    "2023": 150000,
    "2024": 180000
  },
  "user_query": "Analyze our sales performance",
  "timeframe": "Q1 2024"
}
```

**Response:**
```json
{
  "message": "Data submitted. Report generation started.",
  "report_id": "uuid-here"
}
```

#### GET `/get_report/{report_id}`
Get the status and results of a report.

**Response (Generating):**
```json
{
  "status": "generating"
}
```

**Response (Completed):**
```json
{
  "status": "completed",
  "report_text": "Full report text here..."
}
```

## 🏗️ Project Structure

```
qloo-hackathon/
├── main.py              # FastAPI backend 
├── app.py               # Old Flask backend 
├── agent.py             # Marketing report agent with AI logic
├── tools.py             # External API integration tools
├── tool_schema.py       # Tool schemas and descriptions
├── index.html           # Main frontend interface
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variable template
└── README.md           # This file
```

## 🎯 How It Works

1. **User submits data**: Company name, sales data, query, and timeframe through the web interface
2. **Background processing**: FastAPI starts a background task to generate the report
3. **AI analysis**: The agent uses Llama AI to plan which tools to use
4. **Data gathering**: Executes brand analysis, location analysis, and other tools via Qloo API
5. **Report generation**: Llama AI synthesizes all data into a comprehensive business report
6. **Polling**: Frontend polls the backend to check report status
7. **Display results**: Shows the completed report to the user

## 🔧 Development

### Running in development mode

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The `--reload` flag enables auto-reloading on code changes.

### Testing the API

You can test the API using curl:

```bash
# Health check
curl http://localhost:8000/health

# Submit report data
curl -X POST http://localhost:8000/submit_report_data \
  -H "Content-Type: application/json" \
  -d '{
    "company": "Test Company",
    "sales_data": {"2024": 100000},
    "user_query": "Test query",
    "timeframe": "2024"
  }'

# Get report (replace {report_id} with actual ID)
curl http://localhost:8000/get_report/{report_id}
```

## 🚀 Deployment

### Using Uvicorn (Production)

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Using Gunicorn + Uvicorn Workers

```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 🐛 Troubleshooting

### "Module not found" errors
Make sure you've installed all dependencies:
```bash
pip install -r requirements.txt
```

### API Key errors
Verify your `.env` file has the correct API keys and is in the project root.

### CORS errors
Make sure the frontend is making requests to `http://localhost:8000`, not the old production URL.

### Report generation timeouts
The system polls for up to 1 minute. If reports take longer, increase `maxAttempts` in `index.html`.

## 📝 Notes

- This was a hackathon project that wasn't fully working
- Now converted from Flask to FastAPI for better async support
- Uses background tasks to handle long-running report generation
- Frontend uses polling to check report status

## 🤝 Contributing

This is a hackathon demo project. Feel free to fork and improve it!

## 📄 License

MIT License - feel free to use this for learning purposes.
