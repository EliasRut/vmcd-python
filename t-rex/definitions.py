from pydantic import BaseModel
from typing import List

class CollisionBox(BaseModel):
    """
    Define the structure of a collision box object.
    """
    x: int
    y: int
    width: int
    height: int

class Obstacle(BaseModel):
    """
    Class to represent an obstacle in the game.
    """
    collisionBoxes: List[CollisionBox]  # List of collision boxes for the obstacle
    type: str  # Type of the obstacle
    xPos: int  # X position of the obstacle
    yPos: int  # Y position of the obstacle

class ProcessObstaclesCallData(BaseModel):
    """
    Class to represent the data sent to the server for processing obstacles.
    """
    obstacles: List[dict]  # List of obstacles, each represented as a dictionary
    speed: float  # Speed of the t-rex
    isNight: bool  # Indicates whether it is night or not

class ProcessObstaclesCallResponse(BaseModel):
    """
    Class to represent the response from the server after processing obstacles.
    """
    jump: bool  # Indicates whether the t-rex should jump or not

class PlanCallData(BaseModel):
    """
    Class to represent the data sent to the server for processing obstacles.
    """
    obstacles: List[dict]  # List of obstacles, each represented as a dictionary
    initialSpeed: float  # Speed of the t-rex
    acceleration: float  # Acceleration of the t-rex

class PlanCallResponse(BaseModel):
    """
    Class to represent the response from the server after processing obstacles.
    """
    jumpTimes: List[int]  # List of milliseconds relative to the start of the game for when the t-rex should jump

class GetModeResponse(BaseModel):
    """
    Class to represent the response from the server after processing obstacles.
    """
    mode: str  # Mode of the game. Either "live" or "plan"
