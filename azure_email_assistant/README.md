# Azure Email Assistant

A clean, structured implementation of an email processing system using Azure OpenAI API.

## Project Structure

The project follows clean code principles with a modular architecture:

```
azure_email_assistant/
├── core/                 # Core business logic
│   ├── assistant.py      # Assistant implementations
│   └── config.py         # Configuration settings
├── api/                  # API server implementation
│   └── server.py         # Flask API server
├── tests/                # Test suite
│   ├── test_api.py       # API tests
│   └── test_assistant.py # Assistant tests
└── utils/                # Utility functions
```

## Features

- **No Database Dependency**: Simplified architecture with direct processing
- **Clean Code**: Follows SOLID principles with proper separation of concerns
- **Testable Design**: Mock implementations for testing without API calls
- **Type Hints**: Comprehensive type annotations for better code quality
- **Logging**: Proper logging throughout the application

## Usage

### Running the Server

To run the server with the real Azure OpenAI assistant:

```bash
python main.py run
```

To run the server with a mock assistant (for testing without API calls):

```bash
python main.py run --mock
```

### Testing

To run tests against a running server:

```bash
python main.py test
```

Or run tests directly:

```bash
python run_tests_new.py
```

### API Endpoints

- **POST /webhook/email**: Process incoming emails
  - Required JSON payload: `{"from_email": "sender@example.com", "subject": "Email Subject", "body": "Email Body"}`
  - Returns: JSON with response from the assistant

- **GET /health**: Health check endpoint
  - Returns: `{"status": "ok", "timestamp": "..."}`

- **GET /test**: Test endpoint
  - Returns: `{"status": "success", "message": "API server is running correctly", "timestamp": "..."}`

## Configuration

Configuration settings are defined in `core/config.py`. Update the following settings before use:

- **Azure OpenAI API**: Update endpoint, API key, and deployment name
- **API Server**: Update host, port, and secret key
- **Email Settings**: Update SMTP settings if email sending is implemented

## Integration with Power Automate

To integrate with Power Automate:

1. Run the server on a machine accessible to Power Automate
2. Create a Power Automate flow that sends HTTP requests to the `/webhook/email` endpoint
3. Format the request body as shown in the API Endpoints section
4. Process the response as needed in your Power Automate flow
