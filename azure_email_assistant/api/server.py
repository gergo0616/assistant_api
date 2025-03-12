"""
API server for the Azure Email Assistant.
"""
import logging
from datetime import datetime
from typing import Dict, Any, Optional, Tuple, Union

from flask import Flask, request, jsonify, Response

from azure_email_assistant.core.assistant import (
    BaseAssistant, AzureAssistant, MockAssistant, EmailContent
)
from azure_email_assistant.core.config import api_config


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class APIServer:
    """API server for the Azure Email Assistant."""
    
    def __init__(
        self,
        assistant: BaseAssistant,
        host: str = api_config.host,
        port: int = api_config.port,
        secret_key: str = api_config.secret_key
    ):
        """
        Initialize the API server.
        
        Args:
            assistant: Assistant implementation to use
            host: Host to bind the server to
            port: Port to bind the server to
            secret_key: Secret key for Flask
        """
        self.assistant = assistant
        self.host = host
        self.port = port
        
        # Initialize Flask app
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = secret_key
        
        # Register routes
        self._register_routes()
    
    def _register_routes(self) -> None:
        """Register API routes."""
        self.app.add_url_rule(
            '/webhook/email',
            view_func=self._process_email,
            methods=['POST']
        )
        self.app.add_url_rule(
            '/health',
            view_func=self._health_check,
            methods=['GET']
        )
        self.app.add_url_rule(
            '/test',
            view_func=self._test_endpoint,
            methods=['GET']
        )
    
    def _process_email(self) -> Tuple[Response, int]:
        """Handle incoming email webhook."""
        try:
            data = request.get_json()
            
            if not data:
                return self._error_response("No data provided"), 400
            
            from_email = data.get('from_email')
            subject = data.get('subject')
            body = data.get('body')
            
            if not from_email or not subject or not body:
                return self._error_response(
                    "From email, subject, and body are required"
                ), 400
            
            # Process the email
            email = EmailContent(from_email=from_email, subject=subject, body=body)
            result = self.assistant.process_email(email)
            
            return jsonify(result.to_dict()), 200
            
        except Exception as e:
            logger.error(f"Error processing email: {str(e)}")
            return self._error_response(f"Server error: {str(e)}"), 500
    
    def _health_check(self) -> Tuple[Response, int]:
        """Health check endpoint."""
        return jsonify({
            "status": "ok",
            "timestamp": datetime.now().isoformat()
        }), 200
    
    def _test_endpoint(self) -> Tuple[Response, int]:
        """Test endpoint."""
        return jsonify({
            "status": "success",
            "message": "API server is running correctly",
            "timestamp": datetime.now().isoformat()
        }), 200
    
    def _error_response(self, message: str) -> Dict[str, str]:
        """Create an error response."""
        return {
            "status": "error",
            "error": message
        }
    
    def run(self) -> None:
        """Run the API server."""
        self.app.run(host=self.host, port=self.port)


def create_azure_server() -> APIServer:
    """Create an API server with Azure OpenAI assistant."""
    return APIServer(assistant=AzureAssistant())


def create_mock_server() -> APIServer:
    """Create an API server with mock assistant for testing."""
    return APIServer(assistant=MockAssistant())
