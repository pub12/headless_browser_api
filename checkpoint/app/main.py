"""
Main application entry point
"""
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.endpoints import hello
from app.web import routes
from app.config.settings import API_TITLE, API_HOST, API_PORT, logger

# Create FastAPI application
app = FastAPI(title=API_TITLE)

# Mount static files directory
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web", "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Include routers
app.include_router(hello.router, prefix="/api", tags=["api"])
app.include_router(routes.router, tags=["web"])

# Add web route redirection
@app.get("/")
async def root_redirect():
    """Redirect root to web interface"""
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/web")

def start():
    """Start the application server"""
    import uvicorn
    logger.info(f"Starting server at {API_HOST}:{API_PORT}")
    uvicorn.run(app, host=API_HOST, port=API_PORT)

if __name__ == "__main__":
    start() 