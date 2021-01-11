# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 16:32:33 2020

@author: Manuel Camargo
"""
from utils.support import timeit


@timeit(rec_name='TESTING')
def test_method(arg1, **kwargs):
    return arg1 * 2


@timeit
def test_method2(arg1, **kwargs):
    return 'something'


@timeit(rec_name='OTRA')
def test_method3(arg1, **kwargs):
    return 'something else ', True

def execute_tests():

    log = dict()
    
    assert(test_method(2) == 4)
    
    assert((test_method(2, log_time=log) == 4) and ('TESTING' in log.keys()))
    
    assert((test_method2(3, log_time=log) == 'something') and
           ('TEST_METHOD2' in log.keys()))
    
    assert((len(list(test_method3(3, log_time=log))) == 2) and
           ('OTRA' in log.keys()))
