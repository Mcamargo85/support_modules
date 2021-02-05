# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 18:17:10 2020

@author: Manuel Camargo
"""
import tests.read_log as rl
import tests.analyzer_test as ats
import tests.timeit_tests as tit
import tests.timeline_split_tests as tst

if __name__ == "__main__":
    ats.timeseries_test()
    ats.log_test()
    tit.execute_tests()
    tst.split_log_test()
    rl.read_log_test()
