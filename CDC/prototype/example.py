# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 18:41:21 2019

@author: tageldim
"""

import pandas as pd
from sodapy import Socrata

# %%===========================================================================

APIURL = "chronicdata.cdc.gov"
APPTOKEN = "bi9XxFZGt4uWVdqagl6pbdFht"
DATASET_IDENTIFIER = "fn2i-3j6c"

LIMIT = 100000

# %%===========================================================================

# Authenticated client (needed for non-public datasets)
client = Socrata(APIURL, APPTOKEN)

# %%===========================================================================

resp = client.get(DATASET_IDENTIFIER, limit=LIMIT, topic="All Teeth Removed")

# %%===========================================================================








