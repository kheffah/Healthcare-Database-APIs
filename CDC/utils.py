# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 18:41:21 2019

@author: tageldim
"""

import copy
from pandas import DataFrame, concat
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
    if result.shape[0] > 0:
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

    # sort so that most recent data takes precedence
    cfg.YEARS.sort()
    cfg.YEARS = cfg.YEARS[::-1]
    for year in cfg.YEARS + ["mostRecent", ]:
        try:
            os.mkdir(os.path.join(cfg.SAVEPATH, str(year)))
        except FileExistsError:
            pass

    for dat in [cfg.ORAL_HEALTH, cfg.CITIES]:

        components_df_recent = DataFrame()
        N_df_recent = DataFrame()
        percent_df_recent = DataFrame()

        # Extract data for each year and dataset
        for year in cfg.YEARS:

            dataset = copy.deepcopy(dat)
            print("\n===== %d: %s =====" % (year, dataset['name']))
            dataset["filters"]["year"] = year

            # Get datasets
            print("%s: getting table components" % dataset['name'])
            components_df = get_table_components(client, dataset)
            if components_df.shape[0] < 1:
                continue

            # now get actual datset
            N_df, percent_df = get_summary_dfs_from_dataset(
                client, dataset, components_df)

            # merge with most recent if contains new info
            components_df.loc[:, "year"] = year
            new_idxs = set(
                components_df.index) - set(components_df_recent.index)
            components_df_recent = concat(
                (components_df_recent, components_df.loc[new_idxs, :]),
                axis=0, join='outer', sort=False)
            new_cols = set(N_df.columns) - set(N_df_recent.columns)
            N_df_recent = concat(
                (N_df_recent, N_df.loc[:, new_cols]), axis=1, join='outer',
                sort=False)
            percent_df_recent = concat(
                (percent_df_recent, percent_df.loc[:, new_cols]),
                axis=1, join='outer', sort=False)

            # save
            N_df.loc[:, "year"] = year
            SAVEPATH = os.path.join(cfg.SAVEPATH, str(year))
            percent_df.loc[:, "year"] = year
            components_df.to_csv(os.path.join(
                SAVEPATH, "%s_components_%d.csv" % (dataset['name'], year)))
            N_df.to_csv(os.path.join(
                SAVEPATH, "%s_%s_%d.csv" %
                (dataset['name'], dataset['N'], year)))
            percent_df.to_csv(os.path.join(
                SAVEPATH, "%s_%s_%d.csv" %
                (dataset['name'], dataset['val'], year)))

        # save most recent data
        SAVEPATH = os.path.join(cfg.SAVEPATH, "mostRecent")
        components_df_recent.to_csv(os.path.join(
            SAVEPATH, "%s_components_mostRecent.csv" % dataset['name']))
        N_df_recent.to_csv(os.path.join(
            SAVEPATH, "%s_%s_mostRecent.csv" %
            (dataset['name'], dataset['N'])))
        percent_df_recent.to_csv(os.path.join(
            SAVEPATH, "%s_%s_mostRecent.csv" %
            (dataset['name'], dataset['val'])))

# %%===========================================================================
