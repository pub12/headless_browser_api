"""
Data models for the application
"""
from pydantic import BaseModel
 
class HelloResponse(BaseModel):
    """Response model for hello endpoint"""
    message: str 