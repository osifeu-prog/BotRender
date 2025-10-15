#!/usr/bin/env python3
"""
קובץ הרצה ראשי עבור Render - משתמש בקוד הקיים שלך
"""
import os
import sys
import logging

# הוסף את התיקייה הנוכחית ל-PATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import main

if __name__ == '__main__':
    print("🚀 Starting SELA Bot from bot.py...")
    print("📁 Current directory:", os.getcwd())
    print("📄 Files in directory:", [f for f in os.listdir('.') if f.endswith('.py')])
    
    # הרץ את הקוד הקיים שלך
    main()
