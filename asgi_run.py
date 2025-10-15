import os
from uvicorn import run

def main():
    port = int(os.getenv("PORT", "8000"))
    run("server.server:app", host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()