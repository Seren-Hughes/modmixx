# env_example.py
# ===========================================
# MODMIXX ENVIRONMENT VARIABLES EXAMPLE
# ===========================================
# Copy this file to env.py and fill in your actual values
# Never commit the env.py file to version control
# Add env.py to your .gitignore file

import os

# Django Configuration
os.environ.setdefault("SECRET_KEY", "your-50-character-secret-key-here")
os.environ.setdefault("DEBUG", "True")  # Set to False for production
os.environ.setdefault("DATABASE_URL", "postgresql://user:password@localhost:5432/modmixx_db")

# AWS S3 Storage Configuration
os.environ.setdefault("AWS_ACCESS_KEY_ID", "your-aws-access-key-id")
os.environ.setdefault("AWS_SECRET_ACCESS_KEY", "your-aws-secret-access-key")

# Email Configuration (Gmail SMTP)
os.environ.setdefault("EMAIL_HOST_USER", "your-email@gmail.com")
os.environ.setdefault("EMAIL_HOST_PASSWORD", "your-gmail-app-password")

# Google OAuth Configuration
os.environ.setdefault("SOCIAL_AUTH_GOOGLE_OAUTH2_KEY", "your-google-oauth-client-id")
os.environ.setdefault("SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET", "your-google-oauth-client-secret")

# Google Perspective API (Content Moderation)
os.environ.setdefault("PERSPECTIVE_API_KEY", "your-google-perspective-api-key")

# AWS Rekognition Configuration
os.environ.setdefault("AWS_REGION", "eu-west-1")  # Default fallback in settings
os.environ.setdefault("IMAGE_MODERATION_ENABLED", "true")  # true/false
os.environ.setdefault("REKOG_MIN_CONFIDENCE", "80")  # Confidence threshold (0-100)
os.environ.setdefault("REKOGNITION_ACCESS_KEY", "your-rekognition-access-key")
os.environ.setdefault("REKOGNITION_SECRET", "your-rekognition-secret")