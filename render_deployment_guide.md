# Render.com Deployment Guide

This guide explains how to deploy the Azure Email Assistant to Render.com.

## Deployment Steps

1. **Create a Render account**
   - Go to [render.com](https://render.com/) and sign up for an account

2. **Connect your GitHub repository**
   - From your Render dashboard, go to "Blueprints"
   - Click "New Blueprint Instance"
   - Connect your GitHub account
   - Select the repository: `gergo0616/assistant_api`

3. **Configure the Web Service**
   - Render will automatically detect the `render.yaml` file and configure the service
   - Make sure the following settings are applied:
     - Name: `azure-email-assistant`
     - Environment: `Python`
     - Region: Choose the closest to you
     - Branch: `master`
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `python main.py run` (without the `--mock` flag)
     - Plan: Free

4. **Set Environment Variables**
   - In the Render dashboard, go to your web service
   - Click on "Environment"
   - Add the following environment variables:
     - `AZURE_OPENAI_API_KEY`: Your Azure OpenAI API key
     - `AZURE_OPENAI_ENDPOINT`: Your Azure OpenAI endpoint URL (https://andras018923456332.services.ai.azure.com/)

5. **Deploy the Service**
   - Click "Manual Deploy" and select "Deploy latest commit"
   - Render will build and deploy your application

## Verifying Deployment

After deployment, you can verify that the service is running correctly by:

1. **Check the logs**
   - In the Render dashboard, go to your web service
   - Click on "Logs" to see the server logs
   - Verify that it says "Starting API server with Azure OpenAI assistant" (not "with mock assistant")

2. **Test the endpoints**
   - Visit `https://your-service-name.onrender.com/test` in your browser
   - You should see a JSON response with `"status": "success"` and `"mock": false`

3. **Update Power Automate**
   - Update your Power Automate HTTP action to use the new Render.com URL:
     ```
     https://your-service-name.onrender.com/webhook/email
     ```

## Troubleshooting

If you encounter issues with the deployment:

1. **API Key Issues**
   - Verify that the environment variables are set correctly in the Render dashboard
   - Check the logs for any API authentication errors

2. **Application Errors**
   - Check the logs for any application errors
   - You can temporarily enable the mock assistant by changing the start command to `python main.py run --mock` to test if the application itself is working

3. **Cold Start Issues**
   - The free tier of Render.com spins down services after 15 minutes of inactivity
   - The first request after inactivity may take longer to process
   - Consider upgrading to a paid plan for production use
