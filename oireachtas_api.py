#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Set of functions to query the Oireachtas API at
https://api.oireachtas.ie/v1/
"""


from datetime import datetime, date
from utils import fetch_data_from_api_with_cache, create_members_dict,validate_date_range,get_valid_date_input,logger


def filter_bills_sponsored_by(pId):
    """Return bills sponsored by the member with the specified pId.

    :param str pId: The pId value for the member
    :return: List of bill records sponsored by the member
    :rtype: list
    """

    mem = fetch_data_from_api_with_cache("members")
    leg = fetch_data_from_api_with_cache("legislation")

    members_dict = create_members_dict(mem)
    # print(members_dict)

    # Keep prompting the user for a valid pId until one is found or they choose to exit
    while pId not in members_dict:
        logger.error(f"No such member with given pId {pId}")
        print(f"No such member with given pId '{pId}'. Please provide a valid pId or type 'exit' to quit.")
        
        # Prompt the user to re-enter the pId
        pId = input("Enter a valid pId or enter 'exit' to exit the process: ")

        if pId.lower() == 'exit':
            print("Exiting the process...")
            return []

    # At this point, a valid pId will be provided
    logger.info("Member with given pId found")
    sponsor_name = members_dict[pId]

    sponsored_bills = [
        bill['bill'] for bill in leg['results']
        if any(sponsor['sponsor']['by']['showAs'] == sponsor_name
               for sponsor in bill['bill']['sponsors'])
    ]

    return sponsored_bills


def filter_bills_by_last_updated(since_date_str, until_date_str):
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

    since = get_valid_date_input(since_date_str)
    until = get_valid_date_input(until_date_str)

    if not since or not until:
        logger.warning("Exiting the function 'filter_bills_by_last_updated'")
        print("Exiting the function")
        return None

    since, until = validate_date_range(since, until)


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
    # start_time = datetime.now()

    pId = input("Enter the pId of the member: ") # "CatherineArdagh" and "MickBarry" have sponsored some bills

    results = filter_bills_sponsored_by(pId)

    if results:
        logger.info(f"Bills sponsored by the member with given pId '{pId}' are fetched")
        print("Bills sponsored by the member are:")
        for bill in results:
            print(bill["billNo"]) # Remove ["billNo"] to return entire details of the bills

    # # Capture the finish time
    # finish_time = datetime.now()

    # # Calculate the duration
    # duration = finish_time - start_time
    # logger.info(f"Duration for the data fetching and query run: {duration}")

    """_____________________Task Three driver code________________"""

    since_date_str = input("Enter the 'since' date (YYYY-MM-DD): ")
    until_date_str = input("Enter the 'until' date (YYYY-MM-DD) or press enter to fetch data till date: ")

    try:

        # Calling the function with the date range
        bills_updated = filter_bills_by_last_updated(since_date_str, until_date_str)

        # Printing the bill numbers in the filtered bills
        if bills_updated:
            logger.info(f"Bills between are fetched")
            print(
                f"Bills in the range are:")
            for bill in bills_updated:
                print(bill["billNo"]) # Remove ["billNo"] to return entire details of the bills
    except ValueError as e:
        logger.error("Invalid date format")
        print(f"Error: {e}")
