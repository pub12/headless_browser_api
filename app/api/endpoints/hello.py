"""
Hello world endpoint
"""
from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse

from app.models.schemas import HelloResponse
from app.config.settings import APPROVED_IPS, logger

# Create router
router = APIRouter()

@router.post("/hello", response_model=HelloResponse)
async def hello_world(request: Request):
    """
    Hello world endpoint that checks if client IP is approved
    """
    client_ip = request.client.host
    logger.info(f"Request received from IP: {client_ip}")
    
    if client_ip in APPROVED_IPS:
        logger.info(f"Access granted to IP: {client_ip}")
        return {"message": "hello world"}
    else:
        logger.warning(f"Unauthorized access attempt from IP: {client_ip}")
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"X-Status": "Unauthorized"},
            content={"message": "unauthorized"}
        ) 