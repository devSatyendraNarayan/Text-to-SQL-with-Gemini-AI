# Streamlit Secrets Configuration Guide

This file explains how to configure secrets for both local development and Streamlit Cloud deployment.

## For Local Development

Create a file `.streamlit/secrets.toml` with the following content:

```toml
# Gemini AI API Key
GEMINI_API_KEY = "your-gemini-api-key-here"

# Database Configuration
SQL_SERVER = "your-sql-server-address"
SQL_DATABASE = "your-database-name"

# Optional: Only needed if not using Windows Authentication
SQL_USERNAME = "your-username"
SQL_PASSWORD = "your-password"
```

## For Streamlit Cloud Deployment

1. Go to your Streamlit Cloud dashboard
2. Click on your app
3. Click on "Settings" (⚙️)
4. Go to the "Secrets" section
5. Add the same content as above
6. Click "Save"

**Note:** The `.streamlit/secrets.toml` file is gitignored for security.
