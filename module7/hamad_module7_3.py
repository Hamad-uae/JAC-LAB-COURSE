
# Module 7 - Exercise 03: Docker API
# Create a FastAPI server that provides
# server health information and server time.

import os
import time
import shutil

from datetime import datetime, timezone, timedelta
from fastapi import FastAPI


# Create FastAPI application
app = FastAPI(title="Hamad Server Health API")

# Record when the server starts
START_TIME = time.monotonic()


# Home page
@app.get("/")
def home():
    return {
        "message": "Welcome to Hamad Server API",
        "documentation": "/docs"
    }


# POST endpoint to get server information
@app.post("/server-info")
def server_info():

    # Check available disk space
    disk = shutil.disk_usage("/")

    # Calculate how long the API has been running
    uptime = time.monotonic() - START_TIME

    # Get current time in UTC and UAE
    utc_time = datetime.now(timezone.utc)
    uae_timezone = timezone(timedelta(hours=4))
    uae_time = utc_time.astimezone(uae_timezone)

    # Return health information as JSON
    return {
        "health": {
            "status": "running",
            "uptime_seconds": round(uptime, 2),
            "cpu_cores": os.cpu_count(),
            "disk_free_gb": round(
                disk.free / (1024 ** 3), 2
            )
        },
        "server_time_utc": utc_time.isoformat(
            timespec="seconds"
        ),
        "server_time_uae": uae_time.isoformat(
            timespec="seconds"
        )
    }
