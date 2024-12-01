#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import unittest
from datetime import datetime

from oireachtas_api import LEGISLATION_DATASET, MEMBERS_DATASET
from oireachtas_api import (
    load,
    filter_bills_sponsored_by,
    filter_bills_by_last_updated
)


class TestLoadDataset(unittest.TestCase):

    def setUp(self):
        self.expected = json.load(open(MEMBERS_DATASET))

    def test_load_from_file(self):
        loaded = load(MEMBERS_DATASET)
        self.assertEqual(
            len(loaded['results']),
            len(self.expected['results'])
        )

    def test_load_from_url(self):
        loaded = load('https://api.oireachtas.ie/v1/members?limit=50')
        self.assertEqual(
            len(loaded.get('results', [])),
            len(self.expected['results'])
        )


class TestFilterBillsSponsoredBy(unittest.TestCase):

    def test_sponsored(self):
        results = filter_bills_sponsored_by('IvanaBacik')
        self.assertGreaterEqual(len(results), 2)


class TestFilterBillByLastUpdated(unittest.TestCase):

    def test_last_updated(self):
        expected = set(['77', '101', '58', '141', '55', '94', '133', '132',
                        '131', '111', '135', '134', '91', '129', '103', '138',
                        '106', '139'])
        received = {
            bill['billNo']
            for bill in filter_bills_by_last_updated(
                since=datetime(2018, 12, 1), until=datetime(2019, 1, 1)
            )
        }
        self.assertEqual(expected, received)

if __name__ == '__main__':
    unittest.main()
