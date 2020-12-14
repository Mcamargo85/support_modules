# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 18:08:23 2020

@author: Manuel Camargo
"""
import os
import pandas as pd
import analyzers.sim_evaluator as sim 

#%%


def execute_tests():
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
        
    serie1 = pd.read_csv(os.path.join('tests', 'fixtures', 'ia_valdn.csv'))
    serie1['source'] = 'log'
    serie1['run_num'] = 0
    serie2 = pd.read_csv(os.path.join('tests', 'fixtures', 'ia_valdn_gen.csv'))
    serie2['source'] = 'simulation'
    serie2['run_num'] = 1
    serie = pd.concat([serie1, serie2], axis=0, ignore_index=True)
    serie = serie[['caseid', 'timestamp', 'source', 'run_num']]
    serie['timestamp'] =  pd.to_datetime(serie['timestamp'], 
                                         format="%Y-%m-%d %H:%M:%S.%f")
    evaluation = sim.SimilarityEvaluator(serie, parms, 0, dtype='serie')
    evaluation.measure_distance('hour_emd')
    print(evaluation.similarity)
    evaluation.measure_distance('day_emd')
    print(evaluation.similarity)
    evaluation.measure_distance('day_hour_emd')
    print(evaluation.similarity)
    evaluation.measure_distance('cal_emd')
    print(evaluation.similarity)
