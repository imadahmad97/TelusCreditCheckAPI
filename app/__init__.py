"""
The module responsible for initializing the database for the application.

Functions:
    init_db: Initialize the Supabase client's PostgreSQL database for the application.
    
Dependencies:
    - os
    - create_client
    - Client
"""

import os
from supabase import create_client, Client


def init_db():
    """
    Initialize the Supabase client's PostgreSQL database for the application.

    Returns:
        Client: The Supabase client
    """
    url: str = os.getenv("SUPABASE_URL")
    key: str = os.getenv("SUPABASE_KEY")
    supabase: Client = create_client(url, key)
    return supabase
