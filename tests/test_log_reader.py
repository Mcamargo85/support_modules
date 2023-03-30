import os
from unittest import TestCase
from src.readers.log_reader import LogReader

import pandas as pd


class TestLogReader(TestCase):

    def test_load_data_from_file(self):
        # Event log reading
        column_names = {'Case ID': 'caseid', 'Activity': 'task',
                        'lifecycle:transition': 'event_type', 'Resource': 'user'}
        settings = {'timeformat': '%Y-%m-%dT%H:%M:%S.%f',
                    'column_names': column_names,
                    'one_timestamp': False,
                    'filter_d_attrib': True}

        log = LogReader(os.path.join('tests', 'fixtures', 'PurchasingExample.xes'), settings)
        df = pd.DataFrame(log.data)
        self.assertEqual(len(df.columns), 5)
        self.assertEqual(len(df), 10335)

