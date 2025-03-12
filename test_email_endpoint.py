"""
Test script for the email webhook endpoint.
"""
import json
import requests

# Define the API endpoint
url = "http://127.0.0.1:5000/webhook/email"

# Define the test email data
email_data = {
    "from_email": "test@example.com",
    "subject": "Test Email",
    "body": "This is a test email to verify the Azure OpenAI integration."
}

# Send the POST request
print("Sending test email to API...")
response = requests.post(url, json=email_data)

# Print the response
print(f"Status Code: {response.status_code}")
print("Response:")
print(json.dumps(response.json(), indent=2))
