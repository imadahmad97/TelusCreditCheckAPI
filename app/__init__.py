"""
This module contains a funtion to initialize the database connection to Supabase. The function
contains error handling functionality on top of the database connection initialization to ensure
that the connection is properly established.

Functions:
    init_db: Function to initialize the database connection to Supabase.

Dependencies:
    - logging: The logging module for logging messages.
    - os: The OS module for interacting with the operating system.
    - time: The time module for working with time-related functions.
    - app.service.database_service: The service for interacting with the database.
"""

import logging
import os
import time
from .service.database_service import DataBaseService


def init_db() -> DataBaseService:
    """
    Function to initialize the database connection to Supabase. The function contains error handling
    functionality on top of the database connection initialization to ensure that the connection is
    properly established.

    Returns:
        DataBaseService: The database service object for interacting with the database.

    Raises:
        ConnectionError: An error occurred when initializing the connection to Supabase.
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

            logging.info("[DB INIT] Retrying in %d seconds...", delay_seconds)
            time.sleep(delay_seconds)

    return db_service
