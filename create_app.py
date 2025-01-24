import os
import sys
import time
from fastapi import FastAPI
from app.service.database_service import DataBaseService


def create_app() -> tuple[FastAPI, DataBaseService]:
    """
    Create the FastAPI application, initialize the database service with retries,
    and return the FastAPI app instance.
    """
    app = FastAPI()

    max_retries = 3
    delay_seconds = 5

    for attempt in range(1, max_retries + 1):
        try:
            print(f"[DB INIT] Attempt {attempt} to connect to Supabase...")
            db_service = DataBaseService(
                os.getenv("SUPABASE_URL", "supabase"),
                os.getenv("SUPABASE_KEY", "supabase"),
            )
            app.state.db_service = db_service
            print("[DB INIT] Connection successful!")
            break
        except ConnectionError as exc:
            print(f"[DB INIT] Connection attempt {attempt} failed: {exc}")
            if attempt == max_retries:
                print("[DB INIT] Max retries reached. Exiting application.")
                sys.exit(1)
            else:
                print(f"[DB INIT] Retrying in {delay_seconds} seconds...")
                time.sleep(delay_seconds)

    return app, db_service
