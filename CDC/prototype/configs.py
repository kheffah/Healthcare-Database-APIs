# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 20:41:31 2019

@author: tageldim
"""

# %%===========================================================================
# General
# =============================================================================

APIURL = "chronicdata.cdc.gov"
APPTOKEN = "bi9XxFZGt4uWVdqagl6pbdFht"
LIMIT = 100000

SAVEPATH = "C:\\Users\\tageldim\\Desktop\\Healthcare-Database-APIs\\results\\"

# %%===========================================================================
# Specific datasets
# =============================================================================

# BRFSS Table of oral health
# https://www.opendatanetwork.com/dataset/chronicdata.cdc.gov/96er-cudr
ORAL_HEALTH = {
    "name": "OralHealth",
    "filters": {
        "dataset_identifier": "fn2i-3j6c",
        "limit": LIMIT,
        "year": 2017,
        "break_out_category": "Overall",
        "response": "Yes",
    },
    "QUESTIONIDS": None,
}


















