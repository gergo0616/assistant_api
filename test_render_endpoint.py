"""
Test script for the Render.com email webhook endpoint.
"""
import json
import requests

# Define the API endpoint
url = "https://azure-email-assistant.onrender.com/webhook/email"

# Define the test email data
email_data = {
    "from_email": "test@example.com",
    "subject": "Teszt",
    "body": "csaaaa"
}

# Send the POST request
print("Sending test email to Render.com API...")
response = requests.post(url, json=email_data)

# Print the response
print(f"Status Code: {response.status_code}")
print("Response:")
print(json.dumps(response.json(), indent=2))
