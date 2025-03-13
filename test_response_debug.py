import requests
import json
from pprint import pprint

# Test the API endpoint
url = "https://azure-email-assistant.onrender.com/webhook/email"

# Test data
test_data = {
    "from_email": "test@example.com",
    "subject": "Test Email",
    "body": "This is a test email body."
}

# Make the request
response = requests.post(url, json=test_data)

# Print status code
print(f"Status Code: {response.status_code}")

# Print raw response
print("\nRaw Response:")
print(response.text)

# Try to parse as JSON
try:
    json_response = response.json()
    print("\nJSON Response:")
    pprint(json_response)
    
    # Check if 'response' field exists
    if 'response' in json_response:
        print("\nResponse field found!")
        print(json_response['response'])
    else:
        print("\nResponse field NOT found!")
        print("Available fields:", list(json_response.keys()))
except Exception as e:
    print(f"\nError parsing JSON: {e}")
