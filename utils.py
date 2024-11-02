import os
import logging
import json
import requests
from datetime import datetime, date, timedelta


# Configure logging
logging.basicConfig(filename='logs.txt',  # Log file name
                    level=logging.INFO,          # Log level
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


CACHE_EXPIRATION = timedelta(hours=1)  # Cache duration is one hour

CACHE_MEMBERS_FILE = 'api_cache_members.json'
CACHE_LEGISLATION_FILE = 'api_cache_legislation.json'
url_mapping = {
    "members": ("https://api.oireachtas.ie/v1/members", CACHE_MEMBERS_FILE),
    "legislation": ("https://api.oireachtas.ie/v1/legislation", CACHE_LEGISLATION_FILE)
}


def is_cache_valid(cache_time):
    """Check if the cache is still valid based on the expiration duration."""
    current_time = datetime.now()
    return current_time - cache_time < CACHE_EXPIRATION


def fetch_data_from_api_with_cache(data_type):
    """Fetch data from the API and use file-based caching."""
    if data_type not in url_mapping:
        logger.error(f"Invalid data type {data_type}")
        raise ValueError("Invalid data type")

    url, cache_file = url_mapping[data_type]

    # Check if the cache file exists
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            cached_data = json.load(f)

        # Normalize URLs for comparison
        current_url = url.strip()
        cached_url = cached_data['url'].strip()

        logger.info(f"Current URL: '{current_url}'")
        logger.info(f"Cached URL: '{cached_url}'")

        if cached_url == current_url and is_cache_valid(
                datetime.fromisoformat(cached_data['timestamp'])):
            logger.info(f"Using cached data for {data_type}")
            return cached_data['data']
        else:
            logger.info(f"Cache for {data_type} is expired or URL has changed.")
            print("Cache is expired or URL has changed. Fetching new data.")

    # Fetch data from the API
    try:
        logger.info(f"Fetching data from API {data_type}.")
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Write data to the cache file with metadata
        with open(cache_file, 'w') as f:
            json.dump({
                'url': url,
                'timestamp': datetime.now().isoformat(),
                'data': data
            }, f)

        return data

    except requests.exceptions.RequestException as e:
        logger.info(f"An error {e} occurred while fetching data")
        print(f"An error occurred: {e}")
        return None


def create_members_dict(member_data):
    """Create a dictionary of member data for quick lookup."""
    return {member['member']['pId']: member['member']['fullName']
            for member in member_data['results']}


def validate_dates(since, until):
    """Validate and sanitize date inputs."""
    # Ensure both dates are either datetime or date instances
    if not isinstance(since, (datetime, date)):
        raise ValueError(
            f"Invalid since date: {since}. Must be a datetime or date object.")
    if not isinstance(until, (datetime, date)):
        raise ValueError(
            f"Invalid until date: {until}. Must be a datetime or date object.")

    # Ensure since is not after until
    if since > until:
        raise ValueError(
            f"Invalid date range: 'since' date {since} "
            f"cannot be after 'until' date {until}.")