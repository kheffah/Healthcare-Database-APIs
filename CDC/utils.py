# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 18:41:21 2019

@author: tageldim
"""

from pandas import DataFrame
from sodapy import Socrata

import sys
import os
sys.path.insert(0, os.getcwd())

import configs as cfg

# %%===========================================================================
# Methods
# =============================================================================


def get_df_from_filter(client, filters):
    resp = client.get(**filters)
    return DataFrame.from_records(resp)


def get_table_components(client, dataset):
    # formulate soQL query
    # see: https://dev.socrata.com/docs/queries/group.html
    filters = dataset["filters"].copy()
    filters['select'] = ",".join(dataset['to_fetch_schema'])
    filters['group'] = ",".join(dataset['to_fetch_schema'])
    filters['order'] = ",".join(dataset['to_fetch_schema'][:3])
    result = get_df_from_filter(client, filters=filters)
    result.index = result.loc[:, dataset['indicator']]
    return result


def get_summary_dfs_from_dataset(client, dataset, components_df):

    # get all topics if none are specified
    if dataset['all_indicators'] is None:
        dataset['all_indicators'] = list(
            components_df.loc[:, dataset['indicator']])

    # Now we get results table
    N_df = DataFrame()
    percent_df = DataFrame()

    dataset['filters']['select'] = ",".join(dataset['to_fetch'])
    # dataset['filters']['order'] = 'locationabbr'
    dataset['filters']['order'] = dataset['indexrow']

    for idx, indicatorid in enumerate(dataset['all_indicators']):

        indicatorParent = components_df.loc[
            indicatorid, dataset['indicatorParent']]
        shortname = "%s - %s" % (indicatorParent, indicatorid)
        print("%s: get summary df: %s" % (dataset['name'], shortname))

        dataset['filters'][dataset['indicatorParent']] = indicatorParent
        dataset['filters'][dataset['indicator']] = indicatorid

        result = get_df_from_filter(client, filters=dataset['filters'])
        result.index = result.loc[:, dataset['indexrow']]  # index by state
        N_df.loc[:, shortname] = result.loc[:, dataset['N']]
        percent_df.loc[:, shortname] = result.loc[:, dataset['val']]

    return N_df, percent_df


# %%===========================================================================
# Main
# =============================================================================

if __name__ == '__main__':

    # Authenticated client (needed for non-public datasets)
    client = Socrata(cfg.APIURL, cfg.APPTOKEN)

    for dataset in [cfg.ORAL_HEALTH, cfg.CITIES]:

        # first we get dataset components
        print("%s: getting table components" % dataset['name'])
        components_df = get_table_components(client, dataset)
        components_df.to_csv(os.path.join(
            cfg.SAVEPATH, "%s_components.csv" % dataset['name']))

        # Now we get summary tables
        N_df, percent_df = get_summary_dfs_from_dataset(
            client, dataset, components_df)
        N_df.to_csv(os.path.join(
            cfg.SAVEPATH, "%s_sampleSize.csv" % dataset['name']))
        percent_df.to_csv(os.path.join(
            cfg.SAVEPATH, "%s_percent.csv" % dataset['name']))
