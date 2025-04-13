from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Obstacle(BaseModel):
    # Define the structure of an obstacle object here
    pass

class CallData(BaseModel):
    """
    Define the structure of the call data object.
    """
    obstacles: List[dict]  # List of obstacles, each represented as a dictionary
    pass

class CallResponse(BaseModel):
    """
    Define the structure of the call response object.
    """
    jump: bool  # Indicates whether the t-rex should jump or not
    # Add any other fields you need in the response
    pass

# The actual logic to process the obstacles will be implemented in this function
@app.post("/process_obstacles")
def process_obstacles(data: CallData) -> CallResponse:
    """
    Process a list of obstacles and return True if the t-rex should jump, False otherwise.
    """
    # Implement the logic to process the obstacles and determine if the t-rex should jump
    # For now, we will just return True as a placeholder
    return {"jump": False}

@app.get("/")
def root():
    """
    Serve the static/index.html file.
    """
    import os
    from fastapi.responses import FileResponse

    file_path = os.path.join(os.getcwd(), "index.html")
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        return {"error": "File not found"}
    

# Webserver setup to server all static files in the current directory
@app.get("/{file_path:path}")
def static_files(file_path: str):
    """
    Serve static files from the current directory.
    """
    import os
    from fastapi.responses import FileResponse

    file_path = os.path.join(os.getcwd(), file_path)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        return {"error": "File not found"}
# To run the server, use the command:
# uvicorn server:app --reload