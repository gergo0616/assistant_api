# Power Automate Integration Guide

This guide explains how to set up Microsoft Power Automate to work with your Custom Email Automation Assistant System.

## Prerequisites

1. A Microsoft account with access to Power Automate
2. Your Custom Email Automation Assistant API server running and accessible
3. An email account to monitor for incoming messages

## Setup Steps

### 1. Create a New Flow in Power Automate

1. Log in to [Power Automate](https://flow.microsoft.com/)
2. Click on "Create" and select "Automated flow"
3. Name your flow (e.g., "Email Automation Assistant")
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
   - URI: `https://your-api-server.com/webhook/email` (replace with your actual API endpoint)
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

### 4. Add a Condition (Optional)

You may want to add a condition to only process certain emails:

1. Click "+ New step"
2. Search for "Condition" and select it
3. Configure a condition like:
   - Subject contains specific keywords
   - Email is from specific senders
   - Email is not from your assistant email (to prevent loops)

### 5. Save and Test Your Flow

1. Click "Save" in the top right corner
2. Test the flow by sending a test email to the monitored inbox
3. Check the run history to ensure everything is working correctly

## API Endpoints Reference

Your custom API server provides the following endpoints:

### Email Webhook
- **POST /webhook/email**
  - Processes incoming emails
  - Required fields: `from_email`, `subject`, `body`

### Threads
- **POST /v1/threads**
  - Creates a new conversation thread
  - Required fields: `email_address`, `subject`
- **GET /v1/threads/{thread_id}**
  - Retrieves a specific thread

### Messages
- **POST /v1/threads/{thread_id}/messages**
  - Adds a message to a thread
  - Required fields: `role` (user/assistant), `content`
- **GET /v1/threads/{thread_id}/messages**
  - Retrieves all messages in a thread

### Runs
- **POST /v1/threads/{thread_id}/runs**
  - Processes a thread with the AI assistant
- **GET /v1/threads/{thread_id}/runs/{run_id}**
  - Retrieves the status of a run

## Troubleshooting

If your flow isn't working as expected:

1. Check the Power Automate run history for errors
2. Verify your API server is running and accessible
3. Confirm your API key is valid and properly formatted in the HTTP request
4. Check the API server logs for any errors
5. Test the API endpoints directly using a tool like Postman

## Security Considerations

- Keep your API key secure and rotate it regularly
- Consider implementing IP restrictions on your API server
- Use HTTPS for all communications between Power Automate and your API
- Implement rate limiting to prevent abuse
