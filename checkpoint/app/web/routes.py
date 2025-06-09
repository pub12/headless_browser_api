"""
Web frontend routes
"""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

router = APIRouter()

# Setup templates 
templates_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
templates = Jinja2Templates(directory=templates_path)

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Render the index page"""
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "title": "Hello World API Tester"}
    ) 