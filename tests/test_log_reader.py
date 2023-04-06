import os
from unittest import TestCase
from src.readers.log_reader import LogReader
from parameterized import parameterized

import pandas as pd


class TestLogReader(TestCase):

    @parameterized.expand([
        ['purchasing_example', 'PurchasingExample.xes', 5, 10335, False, '%Y-%m-%dT%H:%M:%S.%f'],
        ['confidential_1000', 'confidential_1000.xes', 5, 26886, False, '%Y-%m-%dT%H:%M:%S.%f'],
        ['bpi_2012_no_start_timestamp', 'BPI_2012_no_start_timestamp.csv', 4, 24, True, '%Y-%m-%d %H:%M:%S.%f'],
        ['event_log', 'event_log.csv', 5, 2157, False, '%Y-%m-%d %H:%M:%S.%f'],
        ['production', 'Production.xes.gz', 5, 4938, False, '%Y-%m-%dT%H:%M:%S.%f'],
        ['case_id_int_case_concept_name', 'case_id_int_case_concept_name.xes', 4, 24, True, '%Y-%m-%dT%H:%M:%S.%f']
    ])
    def test_load_data_from_file(self, _name, event_log, cols, rows, one_ts, time_format):
        # Event log reading
        column_names = {'Case ID': 'caseid', 'Activity': 'task',
                        'lifecycle:transition': 'event_type', 'Resource': 'user'}
        settings = {'timeformat': time_format,
                    'column_names': column_names,
                    'one_timestamp': one_ts,
                    'filter_d_attrib': True}

        log = LogReader(os.path.join('tests', 'fixtures', event_log), settings)
        df = pd.DataFrame(log.data)
        self.assertEqual(len(df.columns), cols)
        self.assertEqual(len(df), rows)

