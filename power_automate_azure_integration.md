# Power Automate Integration with Azure OpenAI

This guide explains how to set up Microsoft Power Automate to work with your Custom Email Automation Assistant System using Azure OpenAI.

## Prerequisites

1. A Microsoft account with access to Power Automate
2. Your Custom Email Automation Assistant API server running and accessible
3. An Azure OpenAI resource with API key
4. An email account to monitor for incoming messages

## Setup Steps

### 1. Create a New Flow in Power Automate

1. Log in to [Power Automate](https://flow.microsoft.com/)
2. Click on "Create" and select "Automated flow"
3. Name your flow (e.g., "Email Automation with Azure OpenAI")
4. Select the trigger "When a new email arrives (V3)" from Office 365 Outlook
5. Click "Create"

### 2. Configure the Email Trigger

1. In the trigger settings, configure:
   - Folder: Inbox (or another folder you want to monitor)
   - Include Attachments: No (unless you need attachment processing)
   - Only with Attachments: No
   - Only with Importance: Normal (or your preference)

### 3. Add an HTTP Request Action

1. Click "+ New step"
2. Search for "HTTP" and select "HTTP" action
3. Configure the HTTP request:
   - Method: POST
   - URI: `http://your-api-server:5000/webhook/email` (replace with your actual API endpoint)
   - Headers: 
     ```
     Content-Type: application/json
     Authorization: Bearer your-api-key-here
     ```
   - Body:
     ```json
     {
       "from_email": "@{triggerOutputs()?['body/from']}",
       "subject": "@{triggerOutputs()?['body/subject']}",
       "body": "@{triggerOutputs()?['body/body']}"
     }
     ```

### 4. Add a Condition to Prevent Email Loops

To prevent your system from responding to its own emails (creating an infinite loop):

1. Click "+ New step"
2. Search for "Condition" and select it
3. Configure the condition:
   - Left side: `triggerOutputs()?['body/from']`
   - Operator: `does not contain`
   - Right side: Your assistant's email address (e.g., `your-email@example.com`)

4. In the "If yes" branch, add your HTTP Request action
5. Leave the "If no" branch empty

### 5. Save and Test Your Flow

1. Click "Save" in the top right corner
2. Test the flow by sending a test email to the monitored inbox
3. Check the run history to ensure everything is working correctly

## Detailed Flow Configuration

Here's a more detailed view of how the flow should be configured:

```
Trigger: When a new email arrives (V3)
|
├─ Condition: Email is not from the assistant
|  |
|  └─ If yes
|     |
|     └─ HTTP POST to webhook/email
|        |
|        └─ Body: JSON with from_email, subject, body
|
└─ If no
   |
   └─ (Do nothing to prevent email loops)
```

## Testing the Integration

After setting up the flow:

1. Send a test email to the monitored inbox
2. Check the Power Automate run history to verify the flow executed successfully
3. Verify that your API server received the webhook request (check server logs)
4. Confirm that Azure OpenAI was called and generated a response
5. Check if the response email was sent back to the original sender

## Troubleshooting

If your flow isn't working as expected:

1. Check the Power Automate run history for errors
2. Verify your API server is running and accessible
3. Confirm your API key is valid and properly formatted in the HTTP request
4. Check the API server logs for any errors
5. Test the API endpoints directly using a tool like Postman
6. Verify Azure OpenAI API credentials are correct in your `.env` file

## Security Considerations

- Keep your API key and Azure OpenAI key secure and rotate them regularly
- Consider implementing IP restrictions on your API server
- Use HTTPS for all communications between Power Automate and your API
- Implement rate limiting to prevent abuse
- Monitor usage of your Azure OpenAI resource to control costs

## Advanced Configuration

### Custom System Prompts

You can customize the system prompt used for Azure OpenAI by modifying the `azure_ai_assistant.py` file:

```python
# Add system message with instructions
formatted_messages.append({
    "role": "system",
    "content": (
        "You are an email assistant that helps users by providing helpful, "
        "accurate, and concise responses to their inquiries. Be professional "
        "and courteous in your replies."
        # Add your custom instructions here
    )
})
```

### Email Response Formatting

To customize how email responses are formatted, modify the `email_processor.py` file:

```python
def send_response_email(self, to_email, subject, body):
    # Create the email message
    msg = MIMEMultipart()
    msg["From"] = EMAIL_USERNAME
    msg["To"] = to_email
    msg["Subject"] = subject
    
    # Add custom formatting to the body here
    formatted_body = f"Dear User,\n\n{body}\n\nBest regards,\nYour Assistant"
    
    # Add the body text
    msg.attach(MIMEText(formatted_body, "plain"))
    # ...
```

### Handling Attachments

If you need to process email attachments, modify the Power Automate flow to include attachments and update your API to handle them.
