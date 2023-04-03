import os
from unittest import TestCase
from src.readers.log_reader import LogReader
from parameterized import parameterized

import pandas as pd


class TestLogReader(TestCase):

    @parameterized.expand([
        ['purchasing_example', 'PurchasingExample.xes', 5, 10335, False],
        ['confidential_1000', 'confidential_1000.xes', 5, 26886, False],
        ['bpi_2012_no_start_timestamp', 'BPI_2012_no_start_timestamp.csv', 4, 24, True],
        ['event_log', 'event_log.csv', 5, 2157, False]
    ])
    def test_load_data_from_file(self, _name, event_log, cols, rows, one_ts):
        # Event log reading
        column_names = {'Case ID': 'caseid', 'Activity': 'task',
                        'lifecycle:transition': 'event_type', 'Resource': 'user'}
        settings = {'timeformat': '%Y-%m-%dT%H:%M:%S.%f',
                    'column_names': column_names,
                    'one_timestamp': one_ts,
                    'filter_d_attrib': True}

        log = LogReader(os.path.join('tests', 'fixtures', event_log), settings)
        df = pd.DataFrame(log.data)
        self.assertEqual(len(df.columns), cols)
        self.assertEqual(len(df), rows)

