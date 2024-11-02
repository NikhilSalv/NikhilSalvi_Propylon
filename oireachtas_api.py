#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Set of functions to query the Oireachtas api at
https://api.oireachtas.ie/v1/
"""
import os
from json import *
import requests
from datetime import datetime, date 


def fetch_data_from_api(url):
    try:
        # Send a GET request to the API
        response = requests.get(url)
        
        # Raise an exception for HTTP errors
        response.raise_for_status()
        
        # Parse the JSON response and return it
        return response.json()
    
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
    
    ret = [
        bill['bill'] for bill in leg['results']
        if any(sponsor['sponsor']['by']['showAs'] == sponsor_name for sponsor in bill['bill']['sponsors'])
    ]

    return ret


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

    # Fetch member and legislation data
    mem = fetch_data_from_api(url_members)
    leg = fetch_data_from_api(url_legislation)

    if mem and leg:
        # Create a members dictionary once
        members_dict = create_members_dict(mem)
        
        # Example usage
        pId = "CatherineArdagh"
        result = filter_bills_sponsored_by(pId)
        
        for res in result:
            print(res)

    # Capture the finish time
    finish_time = datetime.now()
    
    # Calculate the duration
    duration = finish_time - start_time
    
    print(f"Duration for the data fetching and query run : {duration}")

    """____________________________Task Three driver code_________________________"""
    
    # Defining the date range for filtering
    since_date = datetime(2024, 9, 30)  # January 1, 2019
    until_date = datetime(2024, 11, 1) # December 31, 2019

    # # Calling the function with the date range
    # bills_updated = filter_bills_by_last_updated(since_date, until_date)

    # # Printing the bill numbers in the filtered bills
    # for bill in bills_updated:
    #     print(bill['billNo'])