<<<<<<< HEAD
# Hello World IP-Protected API

A FastAPI application that checks if the client's IP is in the list of approved IPs before responding with "hello world". This application includes both API endpoints and a web frontend for testing.

## Features

- IP-based access control for API endpoints
- HTML fetching using Playwright with optimized browser pooling
- Web frontend for testing API functionality
- Detailed logging for debugging and monitoring

## Project Structure

```
browser/
├── app/                  # Application package
│   ├── api/              # API endpoints
│   │   └── endpoints/    # API routes
│   ├── config/           # Configuration settings
│   ├── core/             # Core functionality
│   ├── models/           # Data models
│   └── web/              # Web frontend
│       ├── static/       # Static assets
│       └── templates/    # HTML templates
├── main.py               # Entry point
├── README.md
└── requirements.txt
```

## Setup

1. Install the dependencies:
```bash
pip install -r requirements.txt
```

2. Install Playwright browsers:
```bash
playwright install webkit
```

3. Create a `.env` file in the project root with your approved IP addresses:
```
APPROVED_IPS=127.0.0.1,192.168.1.1,10.0.0.1
```

## Running the Application

Start the server with:
```bash
python main.py
```

The application will be available at http://localhost:4113

## API Endpoints

### Hello World Endpoint

- `POST /api/hello` - Returns "hello world" if your IP is authorized

Example:
```bash
curl -X POST http://localhost:4113/api/hello
```

If your IP is in the approved list, you'll get:
```json
{"message": "hello world"}
```

Otherwise, you'll get a 401 Unauthorized response:
```json
{"message": "unauthorized"}
```

### HTML Fetcher Endpoint

- `POST /api/get_html` - Fetches HTML content from a URL using Playwright

Example:
```bash
curl -X POST http://localhost:4113/api/get_html \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

Additional parameters:
```json
{
  "url": "https://example.com",
  "wait_until": "load",       // Options: "load", "domcontentloaded", "networkidle", "selector"
  "selector": "#main-content", // CSS selector to wait for (if wait_until is "selector")
  "timeout": 30000,           // Timeout in milliseconds
  "wait_for": 0,              // Additional wait time in milliseconds
  "images_enabled": true      // Whether to load images
}
```

Response:
```json
{
  "html": "<!DOCTYPE html><html>...</html>",
  "url": "https://example.com",
  "status": "success",
  "fetch_time": 1.25,
  "title": "Example Domain",
  "meta": {
    "description": "Example website",
    "viewport": "width=device-width, initial-scale=1"
  }
}
```

### Browser Pool Management

- `POST /api/init_browser_pool` - Initialize or refresh the browser pool
- `GET /api/browser_pool_status` - Get the current status of the browser pool

## Web Interface

A web interface is available at:
- `http://localhost:4113/web` - Provides a UI to test the API endpoints

## API Documentation

FastAPI provides automatic API documentation at:
- http://localhost:4113/docs
- http://localhost:4113/redoc

## Extending the Application

This structure is designed to be easily extensible:
- Add new API endpoints in `app/api/endpoints/`
- Add new web pages in `app/web/templates/`
- Add new configuration in `app/config/settings.py` 
=======
# headless_browser_api
>>>>>>> 663c8169c7d9282a59c59b49f3f307e47500d639
