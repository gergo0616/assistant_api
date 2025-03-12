"""
Tests for the API server.
"""
import json
import unittest
from unittest.mock import patch

import requests
from flask import Flask
from flask.testing import FlaskClient

from azure_email_assistant.api.server import APIServer
from azure_email_assistant.core.assistant import MockAssistant, EmailContent, AssistantResponse


class TestAPIServer(unittest.TestCase):
    """Test cases for the API server."""
    
    def setUp(self):
        """Set up test environment."""
        self.assistant = MockAssistant()
        self.server = APIServer(assistant=self.assistant)
        self.app = self.server.app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_health_endpoint(self):
        """Test the health endpoint."""
        response = self.client.get('/health')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'ok')
        self.assertIn('timestamp', data)
    
    def test_test_endpoint(self):
        """Test the test endpoint."""
        response = self.client.get('/test')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['message'], 'API server is running correctly')
        self.assertIn('timestamp', data)
    
    def test_email_webhook_valid_data(self):
        """Test the email webhook with valid data."""
        test_data = {
            'from_email': 'test@example.com',
            'subject': 'Test Subject',
            'body': 'This is a test email with a question.'
        }
        
        response = self.client.post(
            '/webhook/email',
            data=json.dumps(test_data),
            content_type='application/json'
        )
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')
        self.assertIn('response', data)
        self.assertIn('request_id', data)
        self.assertIn('timestamp', data)
    
    def test_email_webhook_missing_data(self):
        """Test the email webhook with missing data."""
        test_data = {
            'from_email': 'test@example.com',
            # Missing subject and body
        }
        
        response = self.client.post(
            '/webhook/email',
            data=json.dumps(test_data),
            content_type='application/json'
        )
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['status'], 'error')
        self.assertIn('error', data)
    
    def test_email_webhook_empty_request(self):
        """Test the email webhook with empty request."""
        response = self.client.post(
            '/webhook/email',
            data=json.dumps({}),
            content_type='application/json'
        )
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['status'], 'error')
        self.assertIn('error', data)


if __name__ == '__main__':
    unittest.main()
