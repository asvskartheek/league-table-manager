"""Configuration: environment variables, Supabase client, logging, and timezone."""
import os
import logging
from datetime import timedelta, timezone

from supabase import create_client, Client

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# IST timezone (UTC+5:30)
IST = timezone(timedelta(hours=5, minutes=30))

# Supabase configuration
SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://ichhsthxaegexeogolzz.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
