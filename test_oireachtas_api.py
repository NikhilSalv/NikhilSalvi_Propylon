#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import unittest
from datetime import datetime, timedelta
from unittest.mock import patch, mock_open
from utils import is_cache_valid, fetch_data_from_api_with_cache, create_members_dict, validate_date_range

# from oireachtas_api import LEGISLATION_DATASET, MEMBERS_DATASET

MEMBERS_DATASET = "API_data/API_members_data.json"
LEGISLATION_DATASET = "API_data/API_legislation_data.json"

from oireachtas_api import (
    filter_bills_sponsored_by,
    filter_bills_by_last_updated
)


class TestUtils(unittest.TestCase):

    def test_create_members_dict(self):
        member_data = {
            'results': [
                {'member': {'pId': '1', 'fullName': 'John Doe'}},
                {'member': {'pId': '2', 'fullName': 'Jane Smith'}}
            ]
        }
        expected = {
            '1': 'John Doe',
            '2': 'Jane Smith'
        }
        result = create_members_dict(member_data)
        self.assertEqual(result, expected)

    def test_validate_date_range(self):
        since = datetime(2023, 11, 1)
        until = datetime(2023, 11, 3)
        result = validate_date_range(since, until)
        self.assertEqual(result, (since, until))
        
        with self.assertRaises(ValueError):
            validate_date_range(datetime(2023, 11, 4), until)


# class TestOireachtasAPI(unittest.TestCase):

#     @patch('oireachtas_api.fetch_data_from_api_with_cache')
#     def test_filter_bills_by_last_updated(self, mock_fetch_data):
#         mock_fetch_data.return_value = {'results': [{'bill': {'lastUpdated': '2019-01-01', 'billNo': 'B1'}},
#                                                       {'bill': {'lastUpdated': '2018-12-15', 'billNo': 'B2'}},
#                                                       {'bill': {'lastUpdated': '2019-01-05', 'billNo': 'B3'}}]}
#         since_date_str = datetime(2018, 12, 1)
#         until_date_str = datetime(2019, 1, 1)

#         result = filter_bills_by_last_updated(since_date_str, until_date_str)
#         expected = [{'bill': {'lastUpdated': '2019-01-01', 'billNo': 'B1'}},
#                      {'bill': {'lastUpdated': '2018-12-15', 'billNo': 'B2'}}]
#         self.assertEqual(result, expected)



if __name__ == '__main__':
    unittest.main()
