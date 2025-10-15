#!/usr/bin/env python3
"""
SELA Bot - Main Entry Point with Advanced Debugging
"""
import logging
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    # Initialize advanced debugging
    from advanced_debug import debug
    debug.log_system_info()
    debug.log_database_status()
    debug.log_import_status()
    
    # Import and run main bot
    from main import SelaBot
    debug.log_bot_ready()
    
    print("🚀 Starting SELA Bot with Advanced Debugging...")
    bot = SelaBot()
    bot.run()
    
except Exception as e:
    logging.error(f"💥 Critical error during bot startup: {e}")
    print(f"❌ Bot crashed: {e}")
    sys.exit(1)
