import os
import logging
import json
import requests
from datetime import datetime, date, timedelta
from typing import Optional, Dict, Union


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


def is_cache_valid(cache_time: datetime) -> bool:
    """Check if the cache is still valid based on the expiration duration.

    :param datetime cache_time: The timestamp of when the cache was created, as a datetime object.
    :return: True if the cache is valid (i.e., not expired), False otherwise.
    :rtype: bool
    """
    current_time = datetime.now()
    return current_time - cache_time < CACHE_EXPIRATION


def fetch_data_from_api_with_cache(data_type: str) -> Optional[Union[Dict, list]]:
    """Fetch data from the API and use file-based caching to avoid repeated requests.

    :param str data_type: The type of data to fetch (e.g., 'members' or 'legislation').
    :raises ValueError: If the provided data type is not found in the URL mapping.
    :return: The data from the cache or fetched from the API if the cache is expired or does not exist.
    :rtype: dict or None
    """
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


def create_members_dict(member_data: Dict) -> Dict[str, str]:
    """Create a dictionary of member data for quick lookup by member ID.

    :param dict member_data: The data containing member details, typically a response from the API.
    :return: A dictionary with member IDs (pId) as keys and member full names as values.
    :rtype: dict
    """
    return {member['member']['pId']: member['member']['fullName']
            for member in member_data['results']}


def get_valid_date_input(prompt: str) -> Optional[date]:
    """Prompt the user for a date input and validate its format.

    :param prompt: The input prompt message to show to the user.
    :type prompt: str
    :return: A valid datetime object or None if the user exits.
    :rtype: datetime or None
    """
    while True:
        user_input = prompt
        if not user_input:
            until = date.today()
            return until
        if user_input.lower() == 'exit':
            logger.warning("User exited the function 'filter_bills_by_last_updated'")
            return None
        try:
            valid_date = datetime.strptime(user_input, "%Y-%m-%d").date()
            return valid_date
        except ValueError:
            prompt  = input("Invalid date format. Please enter the date in YYYY-MM-DD format or type 'exit' to quit: ")


def validate_date_range(since: Union[datetime, date], until: Union[datetime, date]) -> Optional[tuple[Union[datetime, date], Union[datetime, date]]]:
    """Validate and sanitize date inputs to ensure they are in the correct format and logical order.

    :param since: The starting date of the range, should be a datetime or date object.
    :type since: datetime or date
    :param until: The ending date of the range, should be a datetime or date object.
    :type until: datetime or date
    :raises ValueError: If the provided `since` or `until` is not a valid date or datetime instance, 
    or if `since` is later than `until`.
    :return: None
    """
    # Ensure since is not after until
    if since >= until:
        logger.warning("Invalid date range")
        raise ValueError(
            f"Invalid date range: 'since' date ({since}) "
            f"cannot be after or equal to 'until' date ({until}).")
    else:
        return since, until