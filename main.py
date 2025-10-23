from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import traceback
import uuid
from typing import Dict, Any, Optional
from agent import generate_report

load_dotenv()

app = FastAPI(title="Sales Report Generator API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory store for reports and their status
report_store: Dict[str, Dict[str, Any]] = {}


# Pydantic models for request validation
class ReportRequest(BaseModel):
    company: str
    sales_data: Dict[str, Any] | str  # Accept both dict and string
    user_query: str
    timeframe: str


class ReportStatusResponse(BaseModel):
    status: str
    report_text: Optional[str] = None
    error: Optional[str] = None


def generate_report_background(report_id: str, company_name: str, sales_data: Any, user_query: str, timeframe: str):
    """
    Background task to generate the report.
    Updates the global report_store with the result or an error message.
    """
    try:
        # Set the status to 'generating'
        report_store[report_id] = {"status": "generating"}
        
        print(f"[Report {report_id}] Starting report generation for {company_name}")
        print(f"[Report {report_id}] Sales data type: {type(sales_data)}")
        print(f"[Report {report_id}] User query: {user_query}")
        print(f"[Report {report_id}] Timeframe: {timeframe}")
        
        # Long-running call to generate the report
        report = generate_report(company_name, sales_data, user_query, timeframe)
        
        if report:
            print(f"[Report {report_id}] Report generated successfully ({len(report)} characters)")
            report_store[report_id] = {"status": "completed", "report_text": report}
        else:
            print(f"[Report {report_id}] Report generation returned empty result")
            report_store[report_id] = {"status": "error", "error": "Report generation returned empty result"}
    except Exception as e:
        print(f"[Report {report_id}] Error in background report generation: {e}")
        traceback.print_exc()
        report_store[report_id] = {"status": "error", "error": f"An error occurred: {str(e)}"}


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Sales Report Generator API",
        "version": "1.0.0",
        "endpoints": {
            "/submit_report_data": "POST - Submit data for report generation",
            "/get_report/{report_id}": "GET - Get report by ID",
            "/health": "GET - Health check"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "API is running"}


@app.post("/submit_report_data")
async def submit_report_data(report_request: ReportRequest, background_tasks: BackgroundTasks):
    """
    Receives user input via a POST request and starts a background task to generate the report.
    Returns a report_id that can be used to check the status.
    """
    try:
        # Generate unique report ID
        report_id = str(uuid.uuid4())
        
        print(f"POST request received. Starting background report generation for report_id: {report_id}")
        
        # Add background task to generate the report
        background_tasks.add_task(
            generate_report_background,
            report_id,
            report_request.company,
            report_request.sales_data,
            report_request.user_query,
            report_request.timeframe
        )
        
        # Immediately return response to client
        return JSONResponse(
            status_code=200,
            content={
                "message": "Data submitted. Report generation started.",
                "report_id": report_id
            }
        )
    
    except Exception as e:
        print(f"Error in submit_report_data: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to submit report data: {str(e)}")


@app.get("/get_report/{report_id}")
async def get_report(report_id: str):
    """
    Retrieves the report from the in-memory store.
    This endpoint will be polled by the frontend to check the status of the report.
    """
    # Check if report_id exists in store
    if report_id not in report_store:
        raise HTTPException(
            status_code=404,
            detail="Report not found. Please ensure you have submitted a valid report request."
        )
    
    report_status = report_store[report_id]
    
    # If still generating, return 202 Accepted
    if report_status['status'] == "generating":
        return JSONResponse(
            status_code=202,
            content={"status": "generating"}
        )
    
    # If completed, return the report and clean up
    if report_status['status'] == "completed":
        report_data = report_store.pop(report_id, None)
        return JSONResponse(
            status_code=200,
            content={
                "status": "completed",
                "report_text": report_data['report_text']
            }
        )
    
    # If error occurred, return error and clean up
    if report_status['status'] == "error":
        error_data = report_store.pop(report_id, None)
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "error": error_data['error']
            }
        )
    
    # Fallback error
    raise HTTPException(status_code=500, detail="Unknown report status")


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    print(f"Global exception handler caught: {exc}")
    traceback.print_exc()
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": str(exc)}
    )


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)

