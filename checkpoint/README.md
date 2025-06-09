# Hello World IP-Protected API

A FastAPI application that checks if the client's IP is in the list of approved IPs before responding with "hello world". This application includes both API endpoints and a web frontend for testing.

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

2. Create a `.env` file in the project root with your approved IP addresses:
```
APPROVED_IPS=127.0.0.1,192.168.1.1,10.0.0.1
```

## Running the Application

Start the server with:
```bash
python main.py
```

The application will be available at http://localhost:4113

## Features

### API Endpoint

The API is available at:
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

### Web Interface

A simple web interface is available at:
- `http://localhost:4113/web` - Provides a UI to test the API

## API Documentation

FastAPI provides automatic API documentation at:
- http://localhost:4113/docs
- http://localhost:4113/redoc

## Extending the Application

This structure is designed to be easily extensible:
- Add new API endpoints in `app/api/endpoints/`
- Add new web pages in `app/web/templates/`
- Add new configuration in `app/config/settings.py` 