#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Set of functions to query the Oireachtas api at
https://api.oireachtas.ie/v1/
"""
import os
import json
from json import *
import requests
from datetime import datetime, date, timedelta


CACHE_FILE = 'api_cache.json'
CACHE_EXPIRATION = timedelta(hours=1) # Cache duration is one hour
CACHE_MEMBERS_FILE = 'api_cache_members.json'
CACHE_LEGISLATION_FILE = 'api_cache_legislation.json'


def is_cache_valid(cache_time):
    """Check if the cache is still valid based on the expiration duration."""

    current_time = datetime.now()
    return current_time - cache_time < CACHE_EXPIRATION


def fetch_data_from_api_with_cache(url):
    """Fetch data from the API and use file-based caching."""
    if url == url_members:
        cache_file = CACHE_MEMBERS_FILE
    elif url == url_legislation:
        cache_file = CACHE_LEGISLATION_FILE
    else:
        raise ValueError("Invalid URL")

    # Check if the cache file exists
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            cached_data = json.load(f)

        # Normalize URLs for comparison
        current_url = url.strip()
        cached_url = cached_data['url'].strip()

        print(f"Current URL: '{current_url}'")
        print(f"Cached URL: '{cached_url}'")

        if cached_url == current_url and is_cache_valid(datetime.fromisoformat(cached_data['timestamp'])):
            print("Using cached data.")
            return cached_data['data']
        else:
            print("Cache is expired or URL has changed. Fetching new data.")

    # Fetch data from the API
    try:
        print("Fetching data from API.")
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
        print(f"An error occurred: {e}")
        return None


def create_members_dict(member_data):
    """Create a dictionary of member data for quick lookup"""
    return {member['member']['pId']: member['member']['fullName'] for member in member_data['results']}


def filter_bills_sponsored_by(pId):
    """Return bills sponsored by the member with the specified pId

    :param str url_members: URL to fetch member data
    :param str url_legislation: URL to fetch legislation data
    :param str pId: The pId value for the member
    :return: List of bill records sponsored by the member
    :rtype: list
    """

    sponsor_name = members_dict.get(pId)

    if not sponsor_name:
        print(f"No member found with pId: {pId}")
        return []
    
    sponsored_bills = [
        bill['bill'] for bill in leg['results']
        if any(sponsor['sponsor']['by']['showAs'] == sponsor_name for sponsor in bill['bill']['sponsors'])
    ]

    return sponsored_bills


def filter_bills_by_last_updated(since, until):
    """Return bills updated within the specified date range

    :param datetime.date since: The lastUpdated value for the bill
        should be greater than or equal to this date
    :param datetime.date until: The lastUpdated value for the bill
        should be less than or equal to this date. If unspecified, until
        will default to today's date
    :return: List of bill records
    :rtype: list

    """
    url_legislation = "https://api.oireachtas.ie/v1/legislation"
    leg = fetch_data_from_api(url_legislation)

    # Check if data was successfully fetched
    if leg is None:
        return []
    
    if until is None:
        until = date.today()

    # Convert input dates to datetime.date if they are not already
    since = since.date() if isinstance(since, datetime) else since
    until = until.date() if isinstance(until, datetime) else until

    # Initialize an empty list to hold bills that match the criteria
    filtered_bills = []

    # Iterate through the bills
    for res in leg['results']:
        bill = res['bill']
        last_updated_str = bill['lastUpdated']

        # Convert the lastUpdated string to a datetime.date object
        last_updated_date = datetime.fromisoformat(last_updated_str).date()
        
        # Check if the lastUpdated date falls within the range
        if since <= last_updated_date <= until:
            filtered_bills.append(bill)
    
    return filtered_bills


if __name__ == "__main__":

    """____________________________Tasks One and Two driver code_________________________"""

    """ * For the offline data, there are two members who have sponsored bills :
    1. Ivana Bacik,
    pId : IvanaBacik

    2. Mick Barry
    pId : MickBarry

    
    * And for the updated data from API, there are two members who have sponsored bills :
    1. Catherine Ardagh,
    pId : CatherineArdagh

    2. Mick Barry
    pId : MickBarry

    """
    
    # Define URLs for member and legislation data
    url_members = "https://api.oireachtas.ie/v1/members"
    url_legislation = "https://api.oireachtas.ie/v1/legislation"

    # Capture the start time
    start_time = datetime.now()

    mem = fetch_data_from_api_with_cache(url_members)
    leg = fetch_data_from_api_with_cache(url_legislation)


    if mem and leg:
        # Create a members dictionary once
        members_dict = create_members_dict(mem)
        
        # Example usage
        pId = "MickBarry"
        results = filter_bills_sponsored_by(pId)

        if results:
            print("Bills sponsored by the member:")
            for bill in results:
                print(bill)
        else:
            print(f"No bills found sponsored by member with pId: {pId}")

    else:
        print("Failed to fetch the necessary data.")

    # Capture the finish time
    finish_time = datetime.now()
    
    # Calculate the duration
    duration = finish_time - start_time
    
    print(f"Duration for the data fetching and query run : {duration}")

    """____________________________Task Three driver code_________________________"""
    
    # Defining the date range for filtering
    since_date = datetime(2024, 9, 30)  # September 30, 2024
    until_date = datetime(2024, 11, 1) # November 1, 2024

    # Calling the function with the date range
    bills_updated = filter_bills_by_last_updated(since_date, until_date)

    # Printing the bill numbers in the filtered bills
    for bill in bills_updated:
        print(bill)