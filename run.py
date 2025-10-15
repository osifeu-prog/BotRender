#!/usr/bin/env python3
import logging, sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from main import SelaBot

def main():
    try:
        print("🚀 Starting SELA Bot...")
        bot = SelaBot()
        bot.run()
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user")
    except Exception as e:
        print(f"❌ Bot crashed: {e}")
        logging.error(f"Bot crash: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
