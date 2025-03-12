"""
Tests for the assistant module.
"""
import unittest
from unittest.mock import patch, MagicMock

import requests

from azure_email_assistant.core.assistant import (
    AzureAssistant, MockAssistant, EmailContent, AssistantResponse
)


class TestMockAssistant(unittest.TestCase):
    """Test cases for the mock assistant."""
    
    def setUp(self):
        """Set up test environment."""
        self.assistant = MockAssistant()
    
    def test_process_email_help(self):
        """Test processing an email with 'help' in the body."""
        email = EmailContent(
            from_email="test@example.com",
            subject="Need Help",
            body="I need help with something."
        )
        
        response = self.assistant.process_email(email)
        
        self.assertEqual(response.status, "success")
        self.assertIn("help", response.response.lower())
        self.assertIsNotNone(response.request_id)
        self.assertIsNotNone(response.timestamp)
    
    def test_process_email_information(self):
        """Test processing an email with 'information' in the body."""
        email = EmailContent(
            from_email="test@example.com",
            subject="Information Request",
            body="I need some information about your services."
        )
        
        response = self.assistant.process_email(email)
        
        self.assertEqual(response.status, "success")
        self.assertIn("information", response.response.lower())
        self.assertIsNotNone(response.request_id)
        self.assertIsNotNone(response.timestamp)
    
    def test_process_email_question(self):
        """Test processing an email with 'question' in the body."""
        email = EmailContent(
            from_email="test@example.com",
            subject="Question",
            body="I have a question about your product."
        )
        
        response = self.assistant.process_email(email)
        
        self.assertEqual(response.status, "success")
        self.assertIn("question", response.response.lower())
        self.assertIsNotNone(response.request_id)
        self.assertIsNotNone(response.timestamp)
    
    def test_process_email_generic(self):
        """Test processing an email with generic content."""
        email = EmailContent(
            from_email="test@example.com",
            subject="General Message",
            body="Just checking in."
        )
        
        response = self.assistant.process_email(email)
        
        self.assertEqual(response.status, "success")
        self.assertIn("received your message", response.response.lower())
        self.assertIsNotNone(response.request_id)
        self.assertIsNotNone(response.timestamp)


class TestAzureAssistant(unittest.TestCase):
    """Test cases for the Azure assistant."""
    
    def setUp(self):
        """Set up test environment."""
        self.assistant = AzureAssistant()
    
    @patch('requests.post')
    def test_process_email_success(self, mock_post):
        """Test successful processing of an email."""
        # Mock successful API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [
                {
                    "message": {
                        "content": "This is a test response from Azure OpenAI."
                    }
                }
            ]
        }
        mock_post.return_value = mock_response
        
        email = EmailContent(
            from_email="test@example.com",
            subject="Test Email",
            body="This is a test email."
        )
        
        response = self.assistant.process_email(email)
        
        self.assertEqual(response.status, "success")
        self.assertEqual(response.response, "This is a test response from Azure OpenAI.")
        self.assertIsNotNone(response.request_id)
        self.assertIsNotNone(response.timestamp)
        
        # Verify the API was called with the correct parameters
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertIn("messages", kwargs["json"])
        self.assertEqual(len(kwargs["json"]["messages"]), 2)
        self.assertEqual(kwargs["json"]["messages"][0]["role"], "system")
        self.assertEqual(kwargs["json"]["messages"][1]["role"], "user")
    
    @patch('requests.post')
    def test_process_email_api_error(self, mock_post):
        """Test handling of API errors."""
        # Mock API error
        mock_post.side_effect = requests.exceptions.RequestException("API error")
        
        email = EmailContent(
            from_email="test@example.com",
            subject="Test Email",
            body="This is a test email."
        )
        
        response = self.assistant.process_email(email)
        
        self.assertEqual(response.status, "error")
        self.assertIn("API request failed", response.error)
        self.assertIsNotNone(response.request_id)
        self.assertIsNotNone(response.timestamp)
    
    @patch('requests.post')
    def test_process_email_empty_response(self, mock_post):
        """Test handling of empty API response."""
        # Mock empty API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": []
        }
        mock_post.return_value = mock_response
        
        email = EmailContent(
            from_email="test@example.com",
            subject="Test Email",
            body="This is a test email."
        )
        
        response = self.assistant.process_email(email)
        
        self.assertEqual(response.status, "error")
        self.assertIn("No response generated", response.error)
        self.assertIsNotNone(response.request_id)
        self.assertIsNotNone(response.timestamp)


if __name__ == '__main__':
    unittest.main()
