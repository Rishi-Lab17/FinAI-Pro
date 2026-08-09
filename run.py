"""
FinAI Pro
Application Entry Point

Run this file to start the FastAPI development server.
"""

import uvicorn


def start_server():
    """
    Starts the FastAPI development server.
    """
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )


if __name__ == "__main__":
    start_server()