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


class TestOireachtasAPI(unittest.TestCase):
    @patch('oireachtas_api.fetch_data_from_api_with_cache')
    @patch('oireachtas_api.create_members_dict')
    def test_returns_non_empty_list_for_valid_pId(self, mock_create_members_dict, mock_fetch_data_from_api):
        # Mock data for members and legislation
        mock_create_members_dict.return_value = {'MickBarry': 'Mick Barry'}
        mock_fetch_data_from_api.side_effect = [
            {'results': [{'id': 'MickBarry'}]},  # mock return for members data
            {'results': [
                {'bill': {'sponsors': [{'sponsor': {'by': {'showAs': 'Mick Barry'}}}]}},
                {'bill': {'sponsors': [{'sponsor': {'by': {'showAs': 'Mick Barry'}}}]}}
            ]}  # mock return for legislation data with multiple matches
        ]
        
        # Call the function with a valid pId
        result = filter_bills_sponsored_by("MickBarry")
        # Assert the result is not empty
        self.assertNotEqual(result, [])
        # Optionally, assert the length of the list
        self.assertGreater(len(result), 0)



if __name__ == '__main__':
    unittest.main()
