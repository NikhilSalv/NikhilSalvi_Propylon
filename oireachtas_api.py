#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Set of functions to query the Oireachtas api at
https://api.oireachtas.ie/v1/
"""
import os
from json import *
from datetime import *
import requests


def filter_bills_sponsored_by(url_members, url_legistaltion, pId):
    """Return bills sponsored by the member with the specified pId

    :param str pId: The pId value for the member
    :return: dict of bill records
    :rtype: dict
    """

    mem = fetch_data_from_api(url_members)
    leg = fetch_data_from_api(url_legistaltion)

    ret = []
    for res in leg['results']:
        p = res['bill']['sponsors']
        for i in p:
            name = i['sponsor']['by']['showAs']
            for result in mem['results']:
                fname = result['member']['fullName']
                rpId = result['member']['pId']
                if fname == name and rpId == pId:
                    ret.append(res['bill'])
    return ret

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
    raise NotImplementedError


if __name__ == "__main__":

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
    pId = "MickBarry"
    url_members = "https://api.oireachtas.ie/v1/members"
    url_legislation = "https://api.oireachtas.ie/v1/legislation"

    result = filter_bills_sponsored_by(url_members, url_legislation, pId)
    print(len(result))