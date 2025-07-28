import os
import time
import sys
from dotenv import load_dotenv
from app import create_app

load_dotenv()

RETRIES = 3
DELAY = 2

def validate_env_vars():
    required = ["OPENAI_API_KEY", "PRINTFUL_API_KEY"]
    missing = [v for v in required if not os.getenv(v)]
    if missing:
        raise EnvironmentError(f"Missing env vars: {', '.join(missing)}")

def main():
    for attempt in range(RETRIES):
        try:
            validate_env_vars()
            app = create_app()
            app.run(debug=True)
            break
        except Exception as e:
            print(f"[Attempt {attempt + 1}] Failed to start: {e}", file=sys.stderr)
            if attempt < RETRIES - 1:
                time.sleep(DELAY)
                DELAY *= 2
            else:
                sys.exit("Max retries reached.")

if __name__ == "__main__":
    main()
