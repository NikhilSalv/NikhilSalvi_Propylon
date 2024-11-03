#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Set of functions to query the Oireachtas API at
https://api.oireachtas.ie/v1/
"""


from datetime import datetime, date
from utils import fetch_data_from_api_with_cache, create_members_dict,validate_dates, logger


def filter_bills_sponsored_by(pId):
    """Return bills sponsored by the member with the specified pId.

    :param str pId: The pId value for the member
    :return: List of bill records sponsored by the member
    :rtype: list
    """

    mem = fetch_data_from_api_with_cache("members")
    leg = fetch_data_from_api_with_cache("legislation")

    members_dict = create_members_dict(mem)
    sponsor_name = members_dict.get(pId)

    if not sponsor_name:
        logger.info(f"No member found with pId: {pId}")
        return []

    sponsored_bills = [
        bill['bill'] for bill in leg['results']
        if any(sponsor['sponsor']['by']['showAs'] == sponsor_name
               for sponsor in bill['bill']['sponsors'])
    ]

    return sponsored_bills


def filter_bills_by_last_updated(since, until):
    """Return bills updated within the specified date range.

    :param datetime.date since: The lastUpdated value for the bill
        should be greater than or equal to this date
    :param datetime.date until: The lastUpdated value for the bill
        should be less than or equal to this date. If unspecified, until
        will default to today's date
    :return: List of bill records
    :rtype: list
    """
    
    leg = fetch_data_from_api_with_cache("legislation")

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

    """_______________Tasks One and Two driver code_____________"""

    # Capture the start time
    start_time = datetime.now()

    # Example usage
    # pId = "MickBarry"
    pId = input("Enter the pId of the member: ")

    results = filter_bills_sponsored_by(pId)

    if results:
        logger.info(f"Bills sponsored by the member with given pId '{pId}' are fetched")
        print("Bills sponsored by the member:")
        for bill in results:
            print(bill["billNo"])
    else:
        print(f"No bills found sponsored by member with pId: {pId}")

    # Capture the finish time
    finish_time = datetime.now()

    # Calculate the duration
    duration = finish_time - start_time
    logger.info(f"Duration for the data fetching and query run: {duration}")

    """_____________________Task Three driver code________________"""

    # # Defining the date range for filtering
    # since_date = datetime(2024, 9, 30)
    # until_date = datetime(2024, 11, 1)

    since_date_str = input("Enter the 'since' date (YYYY-MM-DD): ")
    until_date_str = input("Enter the 'until' date (YYYY-MM-DD): ")

    # Convert the input strings to datetime objects
    

    try:
        # Validate the dates before calling the function
        since_date = datetime.strptime(since_date_str, "%Y-%m-%d")
        until_date = datetime.strptime(until_date_str, "%Y-%m-%d")


        validate_dates(since_date, until_date)

        # Calling the function with the date range
        bills_updated = filter_bills_by_last_updated(since_date, until_date)

        # Printing the bill numbers in the filtered bills
        if bills_updated:
            logger.info(f"Bills between {since_date.date()} and {until_date.date()} are fetched")
            print(
                f"Bills dated from {since_date.date()} to "
                f"{until_date.date()} are:")
            for bill in bills_updated:
                print(bill["billNo"])
    except ValueError as e:
        logger.error("Invalid date format")
        print(f"Error: {e}")
