from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
import base64
from typing import Dict, List, Optional, Any
import json
import time
import platform
import psutil
import datetime
import signal
import socketio
import urllib.parse
import logging
from enum import Enum
import importlib.util
import sys
import pathlib
import importlib.resources

# Import config module
from .config import (
    SERVER_VERSION,
    CLIENT_DIR,
    SCREENSHOTS_DIR,
    SERVER_HOST,
    SERVER_PORT,
    SERVER_URL,
    EXTENSION_TYPE
)

# Setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Function to find the client directory
def find_client_directory():
    """Find the client directory regardless of installation method."""
    # 1. Try the configured path first
    if os.path.exists(CLIENT_DIR) and os.path.exists(os.path.join(CLIENT_DIR, "static")):
        return CLIENT_DIR
        
    # 2. Try importing the client package
    try:
        import client
        client_dir = os.path.dirname(client.__file__)
        if os.path.exists(os.path.join(client_dir, "static")):
            return client_dir
    except ImportError:
        pass
        
    # 3. Look for client relative to the current file
    current_dir = pathlib.Path(__file__).parent
    for parent_level in range(4):  # Check various parent levels
        check_dir = current_dir
        for _ in range(parent_level):
            check_dir = check_dir.parent
            
        candidate = check_dir / "client"
        if candidate.exists() and (candidate / "static").exists():
            return str(candidate)
            
    # 4. Look for client in site-packages
    for path in sys.path:
        client_path = os.path.join(path, "client")
        if os.path.exists(client_path) and os.path.exists(os.path.join(client_path, "static")):
            return client_path
            
    # 5. Try to find using package resources (for wheel installations)
    try:
        import chromecap
        chromecap_dir = os.path.dirname(chromecap.__file__)
        client_path = os.path.join(os.path.dirname(chromecap_dir), "client")
        if os.path.exists(client_path):
            return client_path
    except ImportError:
        pass
    
    # Return the original path as fallback
    return CLIENT_DIR

# Use the function to get the correct client directory
RESOLVED_CLIENT_DIR = find_client_directory()
print(f"Using CLIENT_DIR: {RESOLVED_CLIENT_DIR}")
if not os.path.exists(RESOLVED_CLIENT_DIR):
    print(f"WARNING: CLIENT_DIR not found at {RESOLVED_CLIENT_DIR}")
if not os.path.exists(os.path.join(RESOLVED_CLIENT_DIR, "static")):
    print(f"WARNING: static folder not found at {os.path.join(RESOLVED_CLIENT_DIR, 'static')}")

# Store server start time
SERVER_START_TIME = time.time()
SCREENSHOT_COUNTER = 0
PID = os.getpid()

app = FastAPI(title="Chrome Cap")

# Initialize Socket.IO
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
socket_app = socketio.ASGIApp(sio, app)

# Track connected clients
connected_clients: Dict[str, dict] = {}

# Client tracking for Socket.IO
client_info: Dict[str, dict] = {}
pending_requests: Dict[str, list] = {}

# Socket.IO event handlers


@sio.event
async def connect(sid, environ):
    """Handle client connection"""
    print(f"Client connected: {sid}")
    print(f"Connection environment: {environ.get('HTTP_USER_AGENT', 'Unknown')}")
    
    connected_clients[sid] = {
        'connected_at': datetime.datetime.now().isoformat(),
        'last_heartbeat': datetime.datetime.now().isoformat(),
        'user_agent': environ.get('HTTP_USER_AGENT', 'Unknown')
    }
    
    # Send extension type to client
    await sio.emit('connection_established', {
        'status': 'connected', 
        'client_id': sid,
        'extension_type': EXTENSION_TYPE,
        'server_version': SERVER_VERSION
    })
    
    # Log total number of connected clients
    print(f"Total connected clients: {len(connected_clients)}")


@sio.event
async def disconnect(sid):
    """Handle client disconnection"""
    print(f"Client disconnected: {sid}")
    if sid in connected_clients:
        del connected_clients[sid]
    print(f"Remaining connected clients: {len(connected_clients)}")


@sio.event
async def heartbeat(sid):
    """Handle client heartbeat"""
    if sid in connected_clients:
        connected_clients[sid]['last_heartbeat'] = datetime.datetime.now().isoformat()
        await sio.emit('heartbeat_ack', room=sid)


@sio.event
async def capture_result(sid, data):
    """Handle screenshot capture result from extension"""
    print(f"Received capture result from {sid}")
    
    # Enhanced logging
    if 'request_id' in data:
        print(f"Result for request_id: {data['request_id']}")
    else:
        print("Warning: No request_id in capture result data")
        
    if 'image' in data:
        print(f"Image data received, size: {len(data['image']) // 1024}KB")
    else:
        print("Warning: No image data in capture result")
    
    if 'target_url' in data:
        print(f"Target URL: {data['target_url']}")
        
    # Forward to receive-screenshot endpoint
    try:
        # Make sure we have all required data
        if 'image' not in data:
            print("Error: Missing image data in capture result")
            await sio.emit('capture_error', {
                'status': 'error',
                'message': 'Missing image data in capture result'
            }, room=sid)
            return
            
        response = await receive_screenshot(data)
        print(f"Screenshot processed successfully")
        print(f"Screenshot ID: {response.get('id', 'unknown')}")
        print(f"Screenshot path: {response.get('path', 'unknown')}")
        
        # Send confirmation back to client
        await sio.emit('capture_processed', {
            'status': 'success',
            'screenshot_id': response.get('id'),
            'request_id': data.get('request_id', 'unknown')
        }, room=sid)
    except Exception as e:
        print(f"Error processing screenshot: {e}")
        await sio.emit('capture_error', {
            'status': 'error',
            'message': str(e)
        }, room=sid)


async def broadcast_capture_task(
        target_url: str,
        request_id: str,
        callback_url: str,
        extension_type: str = 'BGPT'):
    """Broadcast a capture task to all connected clients"""
    task_data = {
        'type': 'capture',
        'target_url': target_url,
        'request_id': request_id,
        'callback_url': callback_url,
        'extension_type': extension_type,
        'timestamp': datetime.datetime.now().isoformat()
    }

    # Log the broadcast attempt
    print(f"Broadcasting capture task to {len(connected_clients)} connected clients")
    print(f"Request ID: {request_id}, Target URL: {target_url}")
    
    # If we have connected clients, broadcast the task
    if connected_clients:
        # Print the client IDs for debugging
        client_ids = list(connected_clients.keys())
        print(f"Connected client IDs: {client_ids}")
        
        try:
            await sio.emit('capture_task', task_data)
            print(f"Task broadcasted to clients for request_id: {request_id}")
            return True
        except Exception as e:
            print(f"Error broadcasting task: {e}")
            return False
    else:
        print("No connected clients available for Socket.IO broadcast")
        return False

# CORS configuration to allow requests from the Chrome extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development - restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount(
    "/static",
    StaticFiles(directory=os.path.join(RESOLVED_CLIENT_DIR, "static")),
    name="static"
)
app.mount("/client", StaticFiles(directory=RESOLVED_CLIENT_DIR), name="client")

# Models


class ScreenshotRequest(BaseModel):
    target_url: str
    callback_url: Optional[str] = None


class ScreenshotResponse(BaseModel):
    image: str  # Base64 encoded image


class ServerStatus(BaseModel):
    version: str
    uptime: str
    uptime_seconds: float
    platform: str
    python_version: str
    cpu_usage: float
    memory_usage: Dict[str, float]
    screenshots_count: int
    screenshots_dir: str
    endpoints: List[Dict[str, str]]
    pid: int
    host: str
    port: int
    extension_type: str


class ShutdownResponse(BaseModel):
    success: bool
    message: str


class ExtensionType(str, Enum):
    STANDARD = "STANDARD"
    BGPT = "BGPT"


class ScreenshotListResponse(BaseModel):
    screenshots: List[Dict[str, Any]]


@app.get("/", response_class=HTMLResponse)
async def get_client():
    """Serve the client HTML page."""
    client_html = os.path.join(RESOLVED_CLIENT_DIR, "index.html")
    if not os.path.exists(client_html):
        return f"Client HTML not found at {client_html}. CLIENT_DIR: {RESOLVED_CLIENT_DIR}"
        
    with open(client_html, "r") as f:
        return f.read()


@app.post("/api/receive-screenshot", response_model=dict)
async def receive_screenshot(payload: dict = Body(...)):
    """Receive screenshot from the Chrome extension."""
    global SCREENSHOT_COUNTER

    try:
        # Make sure the screenshots directory exists
        os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

        # Log received payload keys for debugging
        print(f"Received screenshot payload with keys: {list(payload.keys())}")

        # Extract the base64 image data and metadata
        image_data = payload.get("image", "")
        # Use a shorter default for target URLs
        target_url = payload.get("target_url", "ukn")
        # Get request ID if provided
        request_id = payload.get("request_id", "")

        if request_id:
            print(f"Processing screenshot for request ID: {request_id}")
        else:
            print("Warning: No request_id provided in payload")

        if not image_data:
            print("ERROR: No image data provided in payload")
            raise HTTPException(
                status_code=400,
                detail="No image data provided"
            )

        # Check and fix format
        if not image_data.startswith("data:image"):
            print("WARNING: Image data doesn't start with prefix, adding")
            # Assume it's a PNG if no prefix is provided
            image_data = f"data:image/png;base64,{image_data}"

        # Parse image data format
        try:
            image_format = image_data.split(";")[0].split("/")[1]
            image_base64 = image_data.split(",")[1]
        except (IndexError, ValueError) as e:
            print(f"ERROR: Format error: {e}")
            raise HTTPException(
                status_code=400,
                detail="Invalid image data format"
            )

        # Generate a unique filename - include request_id if available
        unique_id = os.urandom(4).hex()
        filename = f"screenshot_{unique_id}.{image_format}"

        # If we have a request ID, include it in a metadata file
        metadata = {
            "id": unique_id,
            "target_url": target_url,
            "request_id": request_id,
            "created": time.time(),
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        filepath = os.path.join(SCREENSHOTS_DIR, filename)
        metadata_filepath = os.path.join(
            SCREENSHOTS_DIR, f"screenshot_{unique_id}.json"
        )

        print(f"Saving screenshot to {filepath}")
        if request_id:
            print(f"With request ID: {request_id}")

        # Get current timestamp
        current_time = time.time()

        # Decode and save to file
        try:
            # Save the image file
            image_bytes = base64.b64decode(image_base64)
            with open(filepath, "wb") as f:
                f.write(image_bytes)

            print(f"Screenshot image saved successfully to {filepath}")

            # Save the metadata file
            with open(metadata_filepath, "w") as f:
                json.dump(metadata, f)
                
            print(f"Screenshot metadata saved to {metadata_filepath}")

            file_size = os.path.getsize(filepath)
            print(f"Screenshot saved successfully. Size: {file_size} bytes")

            # Verify files exist
            if not os.path.exists(filepath):
                print(f"WARNING: Screenshot file not found at {filepath} after saving")
            if not os.path.exists(metadata_filepath):
                print(f"WARNING: Metadata file not found at {metadata_filepath} after saving")

            # Increment screenshot counter
            SCREENSHOT_COUNTER += 1

            result = {
                "status": "success",
                "filename": filename,
                "path": filepath,
                "id": unique_id,
                "size": file_size,
                "url": target_url,
                "request_id": request_id,
                "created": current_time,
                "timestamp": datetime.datetime.fromtimestamp(current_time).strftime(
                    "%Y-%m-%d %H:%M:%S")
            }
            
            print(f"Screenshot processing complete: {result}")
            return result
        except Exception as e:
            print(f"ERROR: Failed to save screenshot: {e}")
            import traceback
            print(traceback.format_exc())
            raise HTTPException(status_code=500, detail=f"Failed to save screenshot: {str(e)}")
    except HTTPException:
        raise
    except Exception as e:
        print(f"ERROR: Unexpected error processing screenshot: {e}")
        import traceback
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Failed to process screenshot: {str(e)}")


@app.get("/api/get-screenshot/{filename}")
async def get_screenshot(filename: str):
    """Get a screenshot by filename."""
    try:
        # Validate filename to prevent path traversal
        if "/" in filename or "\\" in filename:
            raise HTTPException(
                status_code=400,
                detail="Invalid filename"
            )

        filepath = os.path.join(SCREENSHOTS_DIR, filename)
        if not os.path.exists(filepath):
            raise HTTPException(
                status_code=404,
                detail=f"Screenshot {filename} not found"
            )

        # Determine content type based on file extension
        extension = filename.split(".")[-1].lower()
        content_type = {
            "png": "image/png",
            "jpg": "image/jpeg",
            "jpeg": "image/jpeg"
        }.get(extension, "application/octet-stream")

        return FileResponse(
            filepath,
            media_type=content_type,
            filename=filename
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f"ERROR: Failed to get screenshot: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get screenshot: {str(e)}"
        )


@app.get("/api/capture")
async def capture_screenshot(
    url: str,
    request_id: Optional[str] = None,
    extension_type: str = 'BGPT',
    debug: bool = False
):
    """Capture a screenshot of the specified URL"""
    if not request_id:
        request_id = f"task_{int(time.time() * 1000)}"

    print(f"Processing capture request for URL: {url}")
    print(f"Request ID: {request_id}, Extension type: {extension_type}")

    # Build the callback URL
    server_host = os.environ.get("HOST_OVERRIDE", SERVER_HOST)
    server_port = int(os.environ.get("PORT_OVERRIDE", SERVER_PORT))
    callback_url = f"http://{server_host}:{server_port}/api/receive-screenshot"
    
    print(f"Callback URL: {callback_url}")
    print(f"Number of connected Socket.IO clients: {len(connected_clients)}")

    # Try to broadcast via Socket.IO first
    if len(connected_clients) > 0:
        print(f"Attempting to broadcast task via Socket.IO to {len(connected_clients)} clients")
        # List client IDs for debugging
        client_ids = list(connected_clients.keys())
        if len(client_ids) <= 5:  # Only print all IDs if there aren't too many
            print(f"Connected client IDs: {client_ids}")
        else:
            print(f"First 5 client IDs: {client_ids[:5]}")
            
        broadcast_successful = await broadcast_capture_task(
            url, request_id, callback_url, extension_type
        )

        if broadcast_successful:
            print(f"Successfully broadcasted task via Socket.IO for request_id: {request_id}")
            return {
                "status": "task_broadcasted",
                "request_id": request_id,
                "message": "Task broadcasted to connected clients",
                "connected_clients": len(connected_clients)
            }
    else:
        print("No Socket.IO clients connected, will use HTTP fallback mode")

    # Fall back to HTTP approach if no Socket.IO clients or broadcast failed
    print(f"Using HTTP fallback approach for request_id: {request_id}")
    client_url = (
        f"http://{server_host}:{server_port}/client?target={urllib.parse.quote(url)}"
        f"&callback={urllib.parse.quote(callback_url)}"
        f"&request_id={request_id}&extension_type={extension_type}"
    )
    
    print(f"Client URL for fallback HTTP approach: {client_url}")
    
    # For HTTP fallback, we need to guide the user to open the URL in their browser
    return {
        "status": "fallback_http",
        "request_id": request_id,
        "client_url": client_url,
        "message": "No Socket.IO clients connected, falling back to HTTP. Please ensure the BrowserGPT extension is installed and connected."
    }


@app.get("/api/status", response_model=ServerStatus)
async def get_server_status():
    """Get detailed information about the server status."""
    # Calculate uptime
    uptime_seconds = time.time() - SERVER_START_TIME
    uptime = str(datetime.timedelta(seconds=int(uptime_seconds)))

    # Get system information
    cpu_usage = psutil.cpu_percent(interval=0.1)
    memory = psutil.virtual_memory()
    memory_usage = {
        "total_gb": memory.total / (1024**3),
        "available_gb": memory.available / (1024**3),
        "percent": memory.percent
    }

    # Count screenshots
    screenshots_count = len([
        f for f in os.listdir(SCREENSHOTS_DIR)
        if (f.startswith("screenshot_") and
            os.path.isfile(os.path.join(SCREENSHOTS_DIR, f)))
    ])

    # List available endpoints
    endpoints = [
        {"path": "/", "description": "Client HTML page"},
        {"path": "/api/receive-screenshot",
         "description": "Receive screenshot from extension"},
        {"path": "/api/get-screenshot/{filename}",
         "description": "Get a saved screenshot"},
        {"path": "/api/capture", "description": "Initiate screenshot capture"},
        {"path": "/api/status", "description": "Get server status (this endpoint)"},
        {"path": "/api/shutdown", "description": "Shutdown the server"}
    ]

    return ServerStatus(
        version=SERVER_VERSION,
        uptime=uptime,
        uptime_seconds=uptime_seconds,
        platform=platform.platform(),
        python_version=platform.python_version(),
        cpu_usage=cpu_usage,
        memory_usage=memory_usage,
        screenshots_count=screenshots_count,
        screenshots_dir=str(SCREENSHOTS_DIR),
        endpoints=endpoints,
        pid=PID,
        host=SERVER_HOST,
        port=SERVER_PORT,
        extension_type=EXTENSION_TYPE
    )


@app.get("/api/shutdown", response_model=ShutdownResponse)
async def shutdown_server():
    """Shutdown the server gracefully."""
    # This will terminate the process after returning the response
    def shutdown():
        # Give the server time to send the response
        time.sleep(1)
        # Send SIGTERM to self
        os.kill(PID, signal.SIGTERM)

    # Run shutdown in a separate thread to allow response to be sent
    import threading
    threading.Thread(target=shutdown).start()

    return ShutdownResponse(
        success=True,
        message=f"Server shutdown initiated (PID: {PID})"
    )


@app.get("/client", response_class=HTMLResponse)
async def get_client_page():
    """Serve the client HTML page directly from the /client endpoint."""
    with open(os.path.join(RESOLVED_CLIENT_DIR, "index.html"), "r") as f:
        return f.read()


@app.get("/status")
async def check_status():
    """Simple status endpoint for health checks."""
    return {"status": "running"}


@app.post("/shutdown")
async def shutdown_endpoint():
    """Shutdown endpoint for the CLI."""
    return await shutdown_server()


@app.get("/api/screenshots", response_model=ScreenshotListResponse)
async def list_screenshots(
    url: Optional[str] = None,
    limit: Optional[int] = None,
    extension_type: Optional[ExtensionType] = None,
    request_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    List all available screenshots.
    Optional filtering by URL, limit, extension_type, and request_id.
    """
    try:
        screenshots_dir = os.path.join(os.getcwd(), SCREENSHOTS_DIR)
        if not os.path.exists(screenshots_dir):
            os.makedirs(screenshots_dir)

        screenshots = []
        
        print(f"Listing screenshots in directory: {screenshots_dir}")
        print(f"Looking for screenshots with request_id: {request_id}")
        
        # First get a list of all metadata JSON files since they contain request_id
        json_files = [f for f in os.listdir(screenshots_dir) if f.endswith(".json")]
        print(f"Found {len(json_files)} JSON metadata files in screenshots directory")
        
        # First check metadata files if we're filtering by request_id
        if request_id:
            matching_metadata = []
            for json_file in json_files:
                metadata_path = os.path.join(screenshots_dir, json_file)
                try:
                    with open(metadata_path, "r") as f:
                        metadata = json.load(f)
                        if metadata.get("request_id") == request_id:
                            print(f"Found matching metadata file: {json_file} for request_id: {request_id}")
                            metadata["id"] = metadata.get("id", json_file.replace("screenshot_", "").replace(".json", ""))
                            matching_metadata.append(metadata)
                except (json.JSONDecodeError, IOError) as e:
                    print(f"Error reading metadata file {metadata_path}: {e}")
            
            # Check if any metadata files matched the request_id
            if matching_metadata:
                print(f"Found {len(matching_metadata)} metadata files matching request_id: {request_id}")
                for metadata in matching_metadata:
                    # Now verify the screenshot image exists
                    screenshot_id = metadata.get("id")
                    png_path = os.path.join(screenshots_dir, f"screenshot_{screenshot_id}.png")
                    if os.path.exists(png_path):
                        print(f"Found matching PNG file: {png_path}")
                        screenshots.append(metadata)
                    else:
                        print(f"Warning: Matching metadata found but no PNG file at: {png_path}")
        
        # Standard approach - starting from PNG files
        if not request_id or not screenshots:
            # Get a list of all PNG files if we're not using request_id or didn't find matches
            png_files = [f for f in os.listdir(screenshots_dir) if f.endswith(".png")]
            print(f"Found {len(png_files)} PNG files in screenshots directory")

            for filename in png_files:
                if not filename.endswith(".png"):
                    continue

                screenshot_id = filename.replace("screenshot_", "").replace(".png", "")
                
                # Get file path and check if it exists
                filepath = os.path.join(screenshots_dir, filename)
                if not os.path.exists(filepath):
                    print(f"Warning: PNG file {filepath} doesn't exist")
                    continue
                    
                screenshot_data = {
                    "id": screenshot_id,
                    "url": "unknown",
                    "timestamp": 0,
                    "extension_type": "unknown",
                    "request_id": "unknown"
                }

                # Try to read metadata if it exists
                metadata_path = os.path.join(
                    screenshots_dir, f"screenshot_{screenshot_id}.json"
                )

                if os.path.exists(metadata_path):
                    try:
                        with open(metadata_path, "r") as f:
                            metadata = json.load(f)
                            screenshot_data.update(metadata)
                    except (json.JSONDecodeError, IOError) as e:
                        print(f"Error reading metadata file {metadata_path}: {e}")
                else:
                    print(f"Warning: No metadata file found for {screenshot_id}")

                # Apply filters
                if url and screenshot_data.get("url") != url:
                    continue

                if extension_type and screenshot_data.get(
                    "extension_type"
                ) != extension_type.value:
                    continue
                    
                if request_id and screenshot_data.get("request_id") != request_id:
                    continue

                screenshots.append(screenshot_data)

        # Sort by timestamp (newest first)
        def sort_key(x):
            timestamp = x.get("timestamp", 0)
            # Handle both float timestamps and string timestamps
            if isinstance(timestamp, str):
                try:
                    # Try to convert the string timestamp to a datetime and then to a float timestamp
                    dt = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                    return dt.timestamp()
                except (ValueError, TypeError):
                    return 0
            else:
                # If it's already a number or None, convert to float (or 0 if None)
                return float(timestamp or 0)

        screenshots.sort(key=sort_key, reverse=True)
        
        # Log found screenshots for debugging
        print(f"Found {len(screenshots)} screenshots after filtering")
        if len(screenshots) > 0:
            print("First few screenshots:")
            for s in screenshots[:3]:
                print(f"  ID: {s.get('id')}, Request ID: {s.get('request_id', 'unknown')}")

        # Apply limit if specified
        if limit is not None:
            screenshots = screenshots[:limit]

        return {"screenshots": screenshots}
    except Exception as e:
        logger.error(f"Error listing screenshots: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Failed to list screenshots: {str(e)}"
        )


@app.get("/api/screenshot/{filename}")
async def get_screenshot_by_path(filename: str):
    """Get a screenshot by filename."""
    try:
        # Basic validation to prevent path traversal
        if "/" in filename or "\\" in filename:
            raise HTTPException(
                status_code=400,
                detail="Invalid filename. Must not contain path separators."
            )

        if not filename.endswith('.png'):
            filename = f"{filename}.png"

        filepath = os.path.join(SCREENSHOTS_DIR, filename)

        if not os.path.exists(filepath):
            raise HTTPException(
                status_code=404,
                detail=f"Screenshot {filename} not found"
            )

        # Get file modification time
        mod_time = os.path.getmtime(filepath)

        # Read the image file
        with open(filepath, "rb") as f:
            image_data = f.read()

        # Encode image as base64
        encoded_image = base64.b64encode(image_data).decode('utf-8')

        # Determine content type
        content_type = "image/png"

        # Create and return response
        return {
            "id": os.path.splitext(filename)[0],
            "content_type": content_type,
            "timestamp": mod_time,
            "data_url": f"data:{content_type};base64,{encoded_image}"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving screenshot: {str(e)}"
        )


@app.delete("/api/screenshots/{screenshot_id}")
async def delete_screenshot(screenshot_id: str):
    """Delete a screenshot by its ID."""
    try:
        # Look for the file with this ID
        for filename in os.listdir(SCREENSHOTS_DIR):
            if filename.startswith(f"screenshot_{screenshot_id}"):
                filepath = os.path.join(SCREENSHOTS_DIR, filename)

                # Delete the file
                os.remove(filepath)

                return {
                    "status": "success",
                    "message": f"Screenshot {screenshot_id} deleted successfully"
                }

        # If no file was found
        raise HTTPException(
            status_code=404,
            detail=f"Screenshot with ID {screenshot_id} not found"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete screenshot: {str(e)}"
        )


@app.get("/api/raw-screenshot/{screenshot_id}", response_class=FileResponse)
async def get_raw_screenshot(screenshot_id: str):
    """Get a raw binary screenshot by its ID.
    This is useful for clients that want to download the image directly."""
    try:
        # Look for the file with this ID
        filename_pattern = f"screenshot_{screenshot_id}"
        matching_files = [
            f for f in os.listdir(SCREENSHOTS_DIR)
            if f.startswith(filename_pattern) and f.endswith((".png", ".jpg", ".jpeg"))
            and os.path.isfile(os.path.join(SCREENSHOTS_DIR, f))
        ]

        if not matching_files:
            print(f"ERROR: No screenshot found with ID: {screenshot_id}")
            raise HTTPException(
                status_code=404,
                detail=f"Screenshot with ID {screenshot_id} not found"
            )

        # Use the first matching file (should only be one)
        filename = matching_files[0]
        filepath = os.path.join(SCREENSHOTS_DIR, filename)

        # Return the file directly
        return FileResponse(
            filepath,
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"ERROR: Failed to get raw screenshot: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get raw screenshot: {str(e)}"
        )


# Make app available for Socket.IO
app = socket_app


@sio.on("capture_started")
async def handle_capture_started(sid, data):
    """Handle the capture started event from the extension."""
    logger.info(f"Capture started: {data}")
    request_id = data.get("request_id", "unknown")
    url = data.get("url", "unknown")

    # Store the request_id and other metadata
    client_data = client_info.get(sid, {})
    client_data["current_request"] = {
        "request_id": request_id,
        "url": url,
        "start_time": time.time(),
    }
    client_info[sid] = client_data

    # Notify all pending requests for this client
    for future in pending_requests.get(sid, []):
        if not future.done():
            future.set_result({
                "success": True,
                "status": "capture_started",
                "request_id": request_id,
                "url": url
            })


@sio.on("capture_cancel")
async def handle_capture_cancel(sid, data):
    """Handle when a capture is explicitly cancelled by the client."""
    logger.info(f"Capture cancelled by client: {data}")

    client_data = client_info.get(sid, {})
    current_request = client_data.get("current_request", {})

    # Get the request_id if available
    request_id = current_request.get(
        "request_id",
        data.get("request_id", "unknown")
    )

    # Clear the current request
    if "current_request" in client_data:
        del client_data["current_request"]

    # Notify all pending requests for this client
    for future in pending_requests.get(sid, []):
        if not future.done():
            future.set_result({
                "success": False,
                "status": "cancelled",
                "request_id": request_id,
                "message": "Capture was cancelled by the client"
            })
