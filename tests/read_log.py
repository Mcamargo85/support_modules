# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 10:54:25 2021

@author: Manuel Camargo
"""
import os
import readers.log_reader as lr


def read_log_test():
    # Event log reading
    column_names = {'Case ID': 'caseid', 'Activity': 'task',
                    'lifecycle:transition': 'event_type', 'Resource': 'user'}
    settings = {'timeformat': '%Y-%m-%dT%H:%M:%S.%f',
                'column_names': column_names,
                'one_timestamp': False,
                'filter_d_attrib': True}
    
    log = lr.LogReader(os.path.join('tests', 'fixtures', 'PurchasingExample.xes'),
                        settings)
    # log = lr.LogReader(os.path.join('tests', 'fixtures', 'diagram_sim_log_1000.xes'),
    #                     settings)
    print(log.data)
