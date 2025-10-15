#!/usr/bin/env python3
"""
סקריפט ליצירת קובץ .env עם משתנים נדרשים
"""
import os

def create_env_file():
    env_content = """# SELA Bot Environment Variables
# Replace the values with your actual credentials

BOT_TOKEN=your_actual_bot_token_here
ADMIN_ID=123456789

# Generate a secure key with: openssl rand -base64 32
ENCRYPTION_KEY=your_secure_32_byte_base64_key_here=

# Optional API Keys
OPENAI_API_KEY=your_openai_api_key_here
HUGGINGFACE_TOKEN=your_huggingface_token_here

# Render URL (will be auto-set in production)
RENDER_EXTERNAL_URL=https://your-app-name.onrender.com
"""
    
    with open('.env', 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print("✅ Created .env file")
    print("📝 Please edit .env and add your actual credentials")

if __name__ == '__main__':
    create_env_file()
