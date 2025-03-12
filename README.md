# Azure Email Automation Assistant

A clean, structured implementation of an email processing system using Azure OpenAI API.

## System Overview

This system automatically processes incoming emails, sends them to Azure OpenAI API, and replies with the generated response.

### System Components

1. **Email Trigger System**: Monitors inbox for new emails (via Power Automate)
2. **Custom API Service**: Processes email content and forwards to Azure OpenAI
3. **Azure OpenAI Integration**: Generates intelligent responses using Azure's AI models
4. **Email Response System**: Sends the AI-generated response back to the original sender

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

## Setup Instructions

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Configure your settings in `azure_email_assistant/core/config.py`

3. Start the API server:
   ```
   python main.py run
   ```
   
   For testing without Azure OpenAI API calls:
   ```
   python main.py run --mock
   ```

4. Set up Power Automate to trigger the flow when new emails arrive

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

## Azure OpenAI Configuration

You'll need to configure the following Azure OpenAI settings in `azure_email_assistant/core/config.py`:

```python
@dataclass
class AzureConfig:
    """Azure OpenAI API configuration."""
    endpoint: str = "https://your-resource-name.openai.azure.com/"
    api_key: str = "your-api-key-here"
    api_version: str = "2024-08-01-preview"
    deployment: str = "gpt-4o-mini"
    temperature: float = 0.1
    max_tokens: int = 4096
    top_p: float = 0.9
    frequency_penalty: float = 0
    presence_penalty: float = 0
```

## Integration with Power Automate

To integrate with Power Automate:

1. Run the server on a machine accessible to Power Automate
2. Create a Power Automate flow that sends HTTP requests to the `/webhook/email` endpoint
3. Format the request body as shown in the API Endpoints section
4. Process the response as needed in your Power Automate flow
