# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 20:41:31 2019

@author: tageldim
"""

import os

# %%===========================================================================
# General
# =============================================================================

APIURL = "chronicdata.cdc.gov"
APPTOKEN = "bi9XxFZGt4uWVdqagl6pbdFht"
LIMIT = 1000000

METRIC = "crude prevalence"
# METRIC = "age-adjusted prevalence"
SAVEPATH = "C:\\Users\\tageldim\\Desktop\\Healthcare-Database-APIs\\results\\"
SAVEPATH = os.path.join(SAVEPATH, METRIC.replace(' ', '_'))

try:
    os.mkdir(SAVEPATH)
except FileExistsError:
    pass

# %%===========================================================================
# Specific datasets
# =============================================================================

YEARS = [2015, 2016, 2017, 2018]
# YEARS = [2015, ]

# BRFSS Table of oral health
# https://www.opendatanetwork.com/dataset/chronicdata.cdc.gov/96er-cudr
ORAL_HEALTH = {
    "name": "OralHealth",
    # filters for soQL query
    "filters": {
        "dataset_identifier": "fn2i-3j6c",
        "limit": LIMIT,
        # "year": 2015,
        "break_out_category": "Overall",
        "response": "Yes",
        "data_value_type": METRIC.title(),
    },
    # unique metrics to fetch
    "all_indicators": None,
    # fetch columns to get table schema
    "to_fetch_schema": [
        'class', 'topic', 'question',
        'classid', 'topicid', 'questionid', ],
    # the indivisible individual unit (eg single question)
    "indicator": "questionid",
    "indicatorParent": "topic",
    # to fetch for summrary table
    "to_fetch": [
        'topic', 'questionid', 'locationabbr',
        'locationdesc', 'sample_size', 'data_value'],
    # x-index in summrary table (eg state names)
    "indexrow": "locationdesc",
    # key columns to fetch (sample size and percent)
    "N": "sample_size",
    "val": "data_value",
}

# %%===========================================================================

# 500 Cities dataset
# https://dev.socrata.com/foundry/chronicdata.cdc.gov/csmm-fdhi
CITIES = {
    "name": "500Cities",
    # filters for soQL query
    "filters": {
        "dataset_identifier": "csmm-fdhi",
        "limit": LIMIT,
        # "year": 2015,
        "data_value_type": METRIC.capitalize(),
        # "data_value_type": "Age-adjusted prevalence",
        "geographiclevel": "City",
    },
    # unique metrics to fetch
    "all_indicators": None,
    # fetch columns to get table schema
    "to_fetch_schema": [
        'category', 'short_question_text', 'measure',
        'data_value_type', 'categoryid', 'measureid', ],
    # the indivisible individual unit (eg single question)
    "indicator": "measureid",
    "indicatorParent": "category",
    # to fetch for summrary table
    "to_fetch": [
        'category', 'measureid', 'cityname',
        'PopulationCount', 'data_value'],
    # x-index in summrary table (eg state names)
    "indexrow": "cityname",
    # key columns to fetch (sample size and percent)
    "N": "PopulationCount",
    "val": "data_value",
}


# %%===========================================================================




