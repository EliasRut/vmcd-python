from fastapi import FastAPI
from definitions import GetModeResponse, ProcessObstaclesCallData, ProcessObstaclesCallResponse, PlanCallData, PlanCallResponse

app = FastAPI()  

# The actual logic to process the obstacles will be implemented in this function
@app.post("/process_obstacles")
def process_obstacles(data: ProcessObstaclesCallData) -> ProcessObstaclesCallResponse:
    """
    Process a list of obstacles and return True if the t-rex should jump, False otherwise.
    """
    # Implement the logic to process the obstacles and determine if the t-rex should jump
    # For now, we will just return True as a placeholder

    ####################################################################################
    # This is where your code goes                                                     #
    # You can access the obstacles using data.obstacles                                #
    # You can access the speed using data.speed                                        #
    ####################################################################################

    return {"jump": True}


# The actual logic to process the obstacles will be implemented in this function
@app.post("/plan")
def plan(data: PlanCallData) -> PlanCallResponse:
    """
    Process a list of obstacles and return a list of timestamps relative to 0 for when the t-rex
    should jump.
    """
    # Implement the logic to plan for all future obstacles

    ####################################################################################
    # This is where your code goes                                                     #
    # You can access the obstacles using data.obstacles                                #
    # You can access the speed using data.speed                                        #
    ####################################################################################

    return {} # "jumpTimes": [1000, 2000, 3000]}  # Example response with jump times

@app.get("/mode")
def get_mode() -> GetModeResponse:
    """
    Informs the frontend which game mode we want to use.
    """
    return {"mode": "live"}  # Either "live" or "plan"

# Server index.html page under root path
@app.get("/")
def root():
    """
    Serve the index.html file.
    """
    import os
    from fastapi.responses import FileResponse

    file_path = os.path.join(os.getcwd(), "index.html")
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        return {"error": "File not found"}


# Webserver setup to server all other static files in the current directory
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
