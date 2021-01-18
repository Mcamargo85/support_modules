# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 22:06:58 2020

@author: Manuel Camargo
"""
import os
import pandas as pd
import readers.log_reader as lr
import readers.log_splitter as tl

def split_log_test():
    # Event log reading
    column_names = {'Case ID': 'caseid', 'Activity': 'task',
                    'lifecycle:transition': 'event_type', 'Resource': 'user'}
    settings = {'timeformat': '%Y-%m-%dT%H:%M:%S.%f',
                'column_names': column_names,
                'one_timestamp': False,
                'filter_d_attrib': True}
    
    log = lr.LogReader(os.path.join('tests', 'fixtures', 'PurchasingExample.xes'),
                       settings)
    
    splitter = tl.LogSplitter(log.data)
    train, test = splitter.split_log('timeline_contained', 0.8,
                                     settings['one_timestamp'])
    print(len(log.data))
    print(len(train))
    print(len(test))
    
    log_min = pd.DataFrame(log.data).start_timestamp.min()
    log_max = pd.DataFrame(log.data).end_timestamp.max()
    
    train_min = pd.DataFrame(train).start_timestamp.min()
    train_max = pd.DataFrame(train).end_timestamp.max()
    
    test_min = pd.DataFrame(test).start_timestamp.min()
    test_max = pd.DataFrame(test).end_timestamp.max()
    
    print(log_min)
    print(train_min)
    print(train_max)
    print(test_min)
    print(test_max)
    print(log_max)
    
    assert(log_min == train_min)
    assert(log_max == test_max)
    
    assert(train_max < log_max)
    assert(train_max < test_max)
    assert(train_max < test_min)
    print('##################')
    splitter2 = tl.LogSplitter(train)
    train, test = splitter2.split_log('timeline_contained', 0.8,
                                      settings['one_timestamp'])
    print(len(train))
    print(len(test))
    
    print('##################')
    train, test = splitter.split_log('timeline_trace', 0.8,
                                     settings['one_timestamp'])
    print(len(log.data))
    print(len(train))
    print(len(test))
    
    log_min = pd.DataFrame(log.data).start_timestamp.min()
    log_max = pd.DataFrame(log.data).end_timestamp.max()
    
    train_min = pd.DataFrame(train).start_timestamp.min()
    train_max = pd.DataFrame(train).end_timestamp.max()
    
    test_min = pd.DataFrame(test).start_timestamp.min()
    test_max = pd.DataFrame(test).end_timestamp.max()
    
    print(log_min)
    print(train_min)
    print(train_max)
    print(test_min)
    print(test_max)
    print(log_max)
    
    assert(log_min == train_min)
    assert(log_max == test_max)
    
    assert(train_max < log_max)
    assert(train_max < test_max)
    print('##################')
    print(len(pd.DataFrame(log.data).caseid.unique()))
    splitter3 = tl.LogSplitter(log.data)
    train, test = splitter3.split_log('random', 0.8,
                                      settings['one_timestamp'])
    print(len(train.caseid.unique()))
    print(len(test.caseid.unique()))
