"""
Script to test the API endpoints of the running test server.
"""
import requests
import json

def test_health_endpoint():
    """Test the health endpoint."""
    url = "http://localhost:5000/health"
    
    try:
        response = requests.get(url)
        print(f"Health Endpoint Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error testing health endpoint: {str(e)}")
        return False

def test_test_endpoint():
    """Test the test endpoint."""
    url = "http://localhost:5000/test"
    
    try:
        response = requests.get(url)
        print(f"Test Endpoint Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error testing test endpoint: {str(e)}")
        return False

def test_email_webhook_endpoint():
    """Test the email webhook endpoint with mock data."""
    url = "http://localhost:5000/webhook/email"
    
    # Mock email data
    data = {
        "from_email": "test@example.com",
        "subject": "Test Email",
        "body": "This is a test email to verify the webhook endpoint works. I have a question about your services."
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"Email Webhook Endpoint Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error testing email webhook endpoint: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing API endpoints...")
    
    health_result = test_health_endpoint()
    test_result = test_test_endpoint()
    webhook_result = test_email_webhook_endpoint()
    
    print("\nEndpoint Test Results:")
    print(f"Health Endpoint: {'✓ PASSED' if health_result else '✗ FAILED'}")
    print(f"Test Endpoint: {'✓ PASSED' if test_result else '✗ FAILED'}")
    print(f"Email Webhook Endpoint: {'✓ PASSED' if webhook_result else '✗ FAILED'}")
