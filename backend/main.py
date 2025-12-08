"""
Kitchen Simulator API - FastAPI Backend
Main entry point for the kitchen simulator service.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI(
    title="Kitchen Simulator API",
    description="Restaurant service flow simulator with agent orchestration",
    version="0.1.0"
)

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return JSONResponse(
        content={
            "status": "healthy",
            "service": "kitchen-simulator",
            "version": "0.1.0"
        }
    )


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Kitchen Simulator API"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

