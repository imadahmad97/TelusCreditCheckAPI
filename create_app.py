import os
import logging
import time
from fastapi import FastAPI
from app.service.database_service import DataBaseService


class InitializationError(Exception):
    pass


def create_app() -> tuple[FastAPI, DataBaseService]:
    """
    Create the FastAPI application, initialize the database service with retries,
    and return the FastAPI app instance.
    """
    max_retries = 3
    delay_seconds = 5

    for attempt in range(1, max_retries + 1):
        try:
            logging.info("[APP INIT] Attempt %d to initialize FastAPI app...", attempt)
            app = FastAPI()
            break
        except Exception as e:
            logging.warning(
                "[APP INIT] FastAPI initialization attempt %d failed: %s", attempt, e
            )
            if attempt == max_retries:
                logging.error("[APP INIT] Max retries reached. Exiting application.")
                raise InitializationError("Failed to initialize FastAPI app.") from e
            else:
                logging.info("[APP INIT] Retrying in %d seconds...", delay_seconds)
                time.sleep(delay_seconds)

    for attempt in range(1, max_retries + 1):
        try:
            logging.info("[DB INIT] Attempt %d to connect to Supabase...", attempt)
            db_service = DataBaseService(
                os.getenv("SUPABASE_URL", "supabase"),
                os.getenv("SUPABASE_KEY", "supabase"),
            )
            app.state.db_service = db_service
            logging.info("[DB INIT] Connection successful!")
            break
        except Exception as e:
            logging.warning("[DB INIT] Connection attempt %d failed: %s", attempt, e)
            if attempt == max_retries:
                logging.error("[DB INIT] Max retries reached.")
                raise ConnectionError(
                    "Failed to initialize connection to Supabase."
                ) from e
            else:
                logging.info("[DB INIT] Retrying in %d seconds...", delay_seconds)
                time.sleep(delay_seconds)

    return app, db_service
