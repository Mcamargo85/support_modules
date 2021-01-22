# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 18:08:23 2020

@author: Manuel Camargo
"""
import os
import pandas as pd
import analyzers.sim_evaluator as sim
from utils.support import timeit
from copy import deepcopy

def load_parms():
    parms = dict()
    parms['output'] = os.path.join('output_files')
    parms['one_timestamp'] = False  # Only one timestamp in the log
    column_names = {'Case ID': 'caseid',
                    'Activity': 'task',
                    'lifecycle:transition': 'event_type',
                    'Resource': 'user'}
    # Event-log reading options
    parms['read_options'] = {
        'timeformat': '%Y-%m-%dT%H:%M:%S.%f',
        'column_names': column_names,
        'one_timestamp': parms['one_timestamp'],
        'filter_d_attrib': True}
    return parms

def timeseries_test():
    parms = load_parms()
    serie1 = pd.read_csv(os.path.join('tests', 'fixtures', 'ia_valdn.csv'))
    serie2 = pd.read_csv(os.path.join('tests', 'fixtures', 'ia_valdn_gen.csv'))
    serie1 = serie1[['caseid', 'timestamp']]
    serie1['timestamp'] =  pd.to_datetime(serie1['timestamp'], 
                                         format="%Y-%m-%d %H:%M:%S.%f")
    serie2 = serie2[['caseid', 'timestamp']]
    serie2['timestamp'] =  pd.to_datetime(serie2['timestamp'], 
                                         format="%Y-%m-%d %H:%M:%S.%f")
    
    evaluation = sim.SimilarityEvaluator(serie1, serie2, parms, dtype='serie')
    evaluation.measure_distance('day_emd')
    print(evaluation.similarity)
    evaluation.measure_distance('day_hour_emd')
    print(evaluation.similarity)
    evaluation.measure_distance('cal_emd')
    print(evaluation.similarity)

def log_test():
    parms = load_parms()
    event_log = pd.read_csv(os.path.join('tests', 'fixtures', 'event_log.csv'))
    event_log['start_timestamp'] =  pd.to_datetime(event_log['start_timestamp'], 
                                         format="%Y-%m-%d %H:%M:%S.%f")
    event_log['end_timestamp'] =  pd.to_datetime(event_log['end_timestamp'], 
                                         format="%Y-%m-%d %H:%M:%S.%f")
    event_log = event_log[~event_log.task.isin(['Start', 'End'])]
    if pd.api.types.is_numeric_dtype(event_log['caseid']):
        event_log['caseid'] = event_log['caseid']+1
        event_log['caseid'] = event_log['caseid'].astype(str)
    event_log['caseid'] = 'Case' + event_log['caseid']
    # Duplicate
    event_log_2 = deepcopy(event_log)
    # Add columns
    evaluation = sim.SimilarityEvaluator(event_log, event_log_2, parms, max_cases=100)
    measure(evaluation)
    
def log_test_3():
    parms = load_parms()
    event_log = pd.read_csv(os.path.join('tests', 'fixtures', 'event_log.csv'))
    event_log['start_timestamp'] =  pd.to_datetime(event_log['start_timestamp'], 
                                         format="%Y-%m-%d %H:%M:%S.%f")
    event_log['end_timestamp'] =  pd.to_datetime(event_log['end_timestamp'], 
                                         format="%Y-%m-%d %H:%M:%S.%f")
    event_log = event_log[~event_log.task.isin(['Start', 'End'])]
    if pd.api.types.is_numeric_dtype(event_log['caseid']):
        event_log['caseid'] = event_log['caseid']+1
        event_log['caseid'] = event_log['caseid'].astype(str)
    event_log['caseid'] = 'Case' + event_log['caseid']
    # Duplicate
    event_log_2 = deepcopy(event_log)
    # Add columns
    evaluation = sim.SimilarityEvaluator(event_log, event_log_2, parms, max_cases=100)
    measure(evaluation)


def log_test_2():
    parms = load_parms()
    event_log = pd.read_csv(os.path.join('tests', 'fixtures', 'BPI_Challenge_2012_W_Two_TS_test.csv'))
    event_log['start_timestamp'] =  pd.to_datetime(event_log['start_timestamp'], 
                                         format="%Y-%m-%d %H:%M:%S.%f")
    event_log['end_timestamp'] =  pd.to_datetime(event_log['end_timestamp'], 
                                         format="%Y-%m-%d %H:%M:%S.%f")
    event_log = event_log[~event_log.task.isin(['Start', 'End'])]
    event_log['caseid'] = event_log['caseid']+1
    max_c = event_log.caseid.max()
    event_log_c = deepcopy(event_log)
    event_log_c['caseid'] = event_log_c['caseid'] + max_c
    event_log = pd.concat([event_log, event_log_c], axis=0, ignore_index=True)
    event_log['caseid'] = event_log['caseid'].astype(str)
    event_log['caseid'] = 'Case' + event_log['caseid']
    # Duplicate
    event_log_2 = deepcopy(event_log)
    # Add columns
    evaluation = sim.SimilarityEvaluator(event_log, event_log_2, parms)
    measure(evaluation)

@timeit
def measure(evaluation):
    evaluation.measure_distance('mae', verbose=False)
    print(evaluation.similarity)
    evaluation.measure_distance('dl', verbose=True)    
    print(evaluation.similarity)
    evaluation.measure_distance('tsd', verbose=False)    
    print(evaluation.similarity)
    evaluation.measure_distance('dl_mae', verbose=False)    
    print(evaluation.similarity)
    