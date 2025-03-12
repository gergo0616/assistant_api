"""
Script to test the API endpoints of the Azure Email Assistant.
"""
import requests
import json
import argparse
import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def test_health_endpoint(base_url="http://localhost:5000"):
    """Test the health endpoint."""
    url = f"{base_url}/health"
    
    try:
        response = requests.get(url)
        logger.info(f"Health Endpoint Status Code: {response.status_code}")
        logger.info(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        logger.error(f"Error testing health endpoint: {str(e)}")
        return False


def test_test_endpoint(base_url="http://localhost:5000"):
    """Test the test endpoint."""
    url = f"{base_url}/test"
    
    try:
        response = requests.get(url)
        logger.info(f"Test Endpoint Status Code: {response.status_code}")
        logger.info(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        logger.error(f"Error testing test endpoint: {str(e)}")
        return False


def test_email_webhook_endpoint(base_url="http://localhost:5000"):
    """Test the email webhook endpoint with mock data."""
    url = f"{base_url}/webhook/email"
    
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
        logger.info(f"Email Webhook Endpoint Status Code: {response.status_code}")
        logger.info(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        logger.error(f"Error testing email webhook endpoint: {str(e)}")
        return False


def main():
    """Main entry point for the test script."""
    parser = argparse.ArgumentParser(description="Test the Azure Email Assistant API endpoints")
    parser.add_argument(
        "--url", 
        default="http://localhost:5000",
        help="Base URL of the API server (default: http://localhost:5000)"
    )
    parser.add_argument(
        "--skip-webhook", 
        action="store_true",
        help="Skip testing the email webhook endpoint"
    )
    
    args = parser.parse_args()
    base_url = args.url
    
    logger.info(f"Testing API endpoints at {base_url}...")
    
    health_result = test_health_endpoint(base_url)
    test_result = test_test_endpoint(base_url)
    
    results = {
        "Health Endpoint": health_result,
        "Test Endpoint": test_result
    }
    
    if not args.skip_webhook:
        webhook_result = test_email_webhook_endpoint(base_url)
        results["Email Webhook Endpoint"] = webhook_result
    
    logger.info("\nEndpoint Test Results:")
    all_passed = True
    
    for endpoint, passed in results.items():
        status = "PASSED" if passed else "FAILED"
        logger.info(f"{endpoint}: {status}")
        if not passed:
            all_passed = False
    
    if all_passed:
        logger.info("\nAll tests passed successfully!")
        return 0
    else:
        logger.error("\nSome tests failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
