"""
main.py - Entry point for starting the web application via Uvicorn.
Loads environment variables and starts the ASGI server.
"""

from dotenv import load_dotenv
load_dotenv()

import uvicorn
from .app import create_app

app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)