# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 18:41:21 2019

@author: tageldim
"""

from pandas import DataFrame
from sodapy import Socrata

import sys, os
sys.path.insert(0, os.getcwd())

import configs as cfg

# %%===========================================================================
# Methods
# =============================================================================


def get_df_from_filter(client, filters):
    resp = client.get(**filters)
    return DataFrame.from_records(resp)


def get_table_components(client, filters):
    # formulate soQL query
    # see: https://dev.socrata.com/docs/queries/group.html
    to_fetch = [
        'class', 'topic', 'question',
        'classid', 'topicid', 'questionid', ]
    filters['select'] = ",".join(to_fetch)
    filters['group'] = ",".join(to_fetch)
    filters['order'] = ",".join(to_fetch[:3])
    result = get_df_from_filter(client, filters=filters)
    result.index = result.loc[:, "questionid"]
    return result


def get_summary_dfs_from_dataset(client, dataset):

    # get all topics if none are specified
    if dataset['QUESTIONIDS'] is None:
        dataset['QUESTIONIDS'] = list(components_df.loc[:, "questionid"])

    # Now we get results table
    N_df = DataFrame()
    percent_df = DataFrame()

    dataset['filters']['select'] = ",".join([
        'topic', 'questionid', 'locationabbr', 'locationdesc',
        'sample_size', 'data_value'])
    dataset['filters']['order'] = ",".join(['locationabbr'])

    for idx, questionid in enumerate(dataset['QUESTIONIDS']):

        topicname = components_df.loc[questionid, "topic"]
        shortname = "%s - %s" % (topicname, questionid)
        print("%s: get summary df: %s" % (dataset['name'], shortname))

        dataset['filters']["topic"] = topicname
        dataset['filters']["questionid"] = questionid
        result = get_df_from_filter(client, filters=dataset['filters'])
        result.index = result.loc[:, "locationdesc"]  # index by state
        N_df.loc[:, shortname] = result.loc[:, "sample_size"]
        percent_df.loc[:, shortname] = result.loc[:, "data_value"]

    return N_df, percent_df


# %%===========================================================================
# Prepwork
# =============================================================================

# Authenticated client (needed for non-public datasets)
client = Socrata(cfg.APIURL, cfg.APPTOKEN)

# %%===========================================================================
# BRFSS Table of oral health
# =============================================================================

dataset = cfg.ORAL_HEALTH

# first we get dataset components
print("%s: getting table components" % dataset['name'])
components_df = get_table_components(client, filters=dataset["filters"].copy())
components_df.to_csv(os.path.join(
    cfg.SAVEPATH, "%s_components.csv" % dataset['name']))

# Now we get summary tables
N_df, percent_df = get_summary_dfs_from_dataset(client, cfg.ORAL_HEALTH)
N_df.to_csv(os.path.join(
    cfg.SAVEPATH, "%s_sampleSize.csv" % dataset['name']))
percent_df.to_csv(os.path.join(
    cfg.SAVEPATH, "%s_percent.csv" % dataset['name']))

# %%===========================================================================
# BRFSS Table of oral health
# =============================================================================




