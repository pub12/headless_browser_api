"""
Data models for the application
"""
from pydantic import BaseModel, HttpUrl
from typing import Optional, Dict, Any

class HelloResponse(BaseModel):
    """Response model for hello endpoint"""
    message: str

class HtmlRequest(BaseModel):
    """Request model for HTML fetching endpoint"""
    url: HttpUrl
    wait_until: Optional[str] = "domcontentloaded"  # 'load', 'domcontentloaded', 'networkidle', 'selector'
    selector: Optional[str] = None  # CSS selector to wait for if wait_until is 'selector'
    timeout: Optional[int] = 30000  # Timeout in milliseconds
    wait_for: Optional[int] = 0  # Additional wait time in milliseconds
    headers: Optional[Dict[str, str]] = None
    images_enabled: Optional[bool] = True  # Whether to load images
    preserve_img_tags: Optional[bool] = True  # Whether to preserve img tags when images are disabled

class HtmlResponse(BaseModel):
    """Response model for HTML fetching endpoint"""
    html: str
    url: str
    status: str
    fetch_time: float
    title: Optional[str] = None
    meta: Optional[Dict[str, str]] = None 