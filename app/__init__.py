import logging
import os
import time
from .service.database_service import DataBaseService


def init_db() -> DataBaseService:
    """
    Create the FastAPI application, initialize the database service with retries,
    and return the FastAPI app instance.
    """
    max_retries = 5
    delay_seconds = 5

    for attempt in range(1, max_retries + 1):
        try:
            logging.info("[DB INIT] Attempt %d to connect to Supabase...", attempt)
            db_service = DataBaseService(
                os.getenv("SUPABASE_URL", "supabase"),
                os.getenv("SUPABASE_KEY", "supabase"),
            )
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

    return db_service
