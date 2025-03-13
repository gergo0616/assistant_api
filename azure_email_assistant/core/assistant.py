"""
Assistant implementations for the Azure Email Assistant.
"""
import json
import logging
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Any, Optional

import requests

from azure_email_assistant.core.config import azure_config


logger = logging.getLogger(__name__)


@dataclass
class EmailContent:
    """Email content to process."""
    from_email: str
    subject: str
    body: str


@dataclass
class AssistantResponse:
    """Response from the assistant."""
    status: str
    response_text: Optional[str] = None
    error: Optional[str] = None
    request_id: str = ""
    timestamp: str = ""
    
    def __post_init__(self):
        """Set timestamp if not provided."""
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()
        if not self.request_id:
            self.request_id = str(uuid.uuid4())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = {
            "status": self.status,
            "request_id": self.request_id,
            "timestamp": self.timestamp
        }
        
        if self.response_text:
            result["response"] = self.response_text
        
        if self.error:
            result["error"] = self.error
            
        return result


class BaseAssistant(ABC):
    """Base assistant interface."""
    
    @abstractmethod
    def process_email(self, email: EmailContent) -> AssistantResponse:
        """Process an email and generate a response."""
        pass
    
    def _format_messages(self, email: EmailContent) -> List[Dict[str, str]]:
        """Format email content into messages for the API."""
        system_message = (
            "You will receive an email subject and a body. As an assistant, you can reply using only what you have in the documents. Write a professional and precise reply based on the subject and body of the email. Begin by greeting the sender appropriately, considering the tone and context of their original message. Do not refer to the document where you found the answer. If the information is unavailable in the documents, reply that you cannot help with that, and an agent will get back to the user soon; again, do not say that the information is not available in the documents. Add the <br> tag when a line breaks; it will help me to format the output. Conclude the email with a standard signature that includes the following information: Name: Gergő Krucsai and Company: SMP Solution."
        )
        
        user_message = (
            f"From: {email.from_email}\n"
            f"Subject: {email.subject}\n"
            f"Body: {email.body}\n\n"
            "Please draft a response to this email."
        )
        
        return [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]


class AzureAssistant(BaseAssistant):
    """Azure OpenAI assistant implementation."""
    
    def __init__(self, config=azure_config):
        """Initialize with configuration."""
        self.config = config
    
    def process_email(self, email: EmailContent) -> AssistantResponse:
        """
        Process an email and generate a response using Azure OpenAI.
        
        Args:
            email: Email content to process
            
        Returns:
            AssistantResponse with the generated response or error
        """
        try:
            # Format messages for Azure OpenAI API
            formatted_messages = self._format_messages(email)
            
            # Prepare request to Azure OpenAI
            request_url = (
                f"{self.config.endpoint}openai/deployments/{self.config.deployment}"
                f"/chat/completions?api-version={self.config.api_version}"
            )
            
            headers = {
                "Content-Type": "application/json",
                "api-key": self.config.api_key
            }
            
            payload = {
                "messages": formatted_messages,
                "model": self.config.deployment,
                "temperature": self.config.temperature,
                "max_tokens": self.config.max_tokens,
                "top_p": self.config.top_p,
                "frequency_penalty": self.config.frequency_penalty,
                "presence_penalty": self.config.presence_penalty,
                "user": str(uuid.uuid4())
            }
            
            # Make request to Azure OpenAI
            response = requests.post(
                request_url,
                headers=headers,
                json=payload,
                timeout=180
            )
            
            # Check for successful response
            response.raise_for_status()
            
            # Parse response
            response_data = response.json()
            
            # Extract assistant message
            assistant_message = response_data["choices"][0]["message"]["content"]
            
            # Clean the response to remove thinking section
            cleaned_response = self._clean_response(assistant_message)
            
            return AssistantResponse(
                status="success",
                response_text=cleaned_response
            )
            
        except requests.exceptions.RequestException as e:
            error_message = f"API request failed: {str(e)}"
            logger.error(error_message)
            return AssistantResponse(status="error", error=error_message)
            
        except (KeyError, IndexError, json.JSONDecodeError) as e:
            error_message = f"Error parsing API response: {str(e)}"
            logger.error(error_message)
            return AssistantResponse(status="error", error=error_message)
            
        except Exception as e:
            error_message = f"Unexpected error: {str(e)}"
            logger.error(error_message)
            return AssistantResponse(status="error", error=error_message)

    def _clean_response(self, response: str) -> str:
        """Remove thinking section from response.
        
        Args:
            response: Raw response from Azure OpenAI
            
        Returns:
            Cleaned response with thinking section removed
        """
        # Check if the response has a clear thinking section followed by actual content
        if '<think>' in response and '</think>' in response:
            # Extract content after the closing think tag
            think_end = response.find('</think>') + len('</think>')
            # Return everything after the closing think tag, removing any leading whitespace or newlines
            return response[think_end:].lstrip()
        
        # Look for common patterns that indicate the transition from thinking to response
        transition_markers = [
            # Hungarian greetings
            'Kedves ',
            'Tisztelt ',
            # English greetings
            'Dear ',
            'Hello ',
            'Hi ',
            # Email formatting
            'Subject:',
            # Multiple newlines often separate thinking from response
            '\n\n\n'
        ]
        
        # Find the earliest occurrence of any transition marker
        earliest_pos = len(response)
        earliest_marker = None
        
        for marker in transition_markers:
            pos = response.find(marker)
            if pos != -1 and pos < earliest_pos:
                earliest_pos = pos
                earliest_marker = marker
        
        # If we found a marker, extract everything from that point
        if earliest_marker:
            # For greetings and subject lines, include the marker
            if earliest_marker in ['Kedves ', 'Tisztelt ', 'Dear ', 'Hello ', 'Hi ', 'Subject:']:
                return response[earliest_pos:].strip()
            # For newlines, skip the marker
            else:
                return response[earliest_pos + len(earliest_marker):].strip()
        
        # If no clear transition is found, try to find the last paragraph
        # This is a fallback for cases where the thinking isn't clearly separated
        paragraphs = response.split('\n\n')
        if len(paragraphs) > 1:
            # Return the last few paragraphs (likely the actual response)
            return '\n\n'.join(paragraphs[-2:]).strip()
        
        # If all else fails, return the original response
        return response


class MockAssistant(BaseAssistant):
    """Mock assistant for testing."""
    
    def process_email(self, email: EmailContent) -> AssistantResponse:
        """
        Process an email and generate a mock response.
        
        Args:
            email: Email content to process
            
        Returns:
            AssistantResponse with a mock response
        """
        # Generate a simple mock response
        mock_response = (
            f"Thank you for your email regarding '{email.subject}'.\n\n"
            f"I have received your message and will get back to you shortly.\n\n"
            f"Best regards,\nAI Assistant"
        )
        
        return AssistantResponse(
            status="success",
            response_text=mock_response
        )
