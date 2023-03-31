import os
from unittest import TestCase
from src.readers.log_reader import LogReader
from parameterized import parameterized

import pandas as pd


class TestLogReader(TestCase):

    @parameterized.expand([
        ['purchasing_example', 'PurchasingExample.xes', 5, 10335],
        ['confidential_1000', 'confidential_1000.xes', 5, 26886],
    ])
    def test_load_data_from_file(self, _name, event_log, cols, rows):
        # Event log reading
        column_names = {'Case ID': 'caseid', 'Activity': 'task',
                        'lifecycle:transition': 'event_type', 'Resource': 'user'}
        settings = {'timeformat': '%Y-%m-%dT%H:%M:%S.%f',
                    'column_names': column_names,
                    'one_timestamp': False,
                    'filter_d_attrib': True}

        log = LogReader(os.path.join('tests', 'fixtures', event_log), settings)
        df = pd.DataFrame(log.data)
        self.assertEqual(len(df.columns), cols)
        self.assertEqual(len(df), rows)

