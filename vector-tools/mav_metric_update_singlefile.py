import os
import re
import sys

import pandas as pd
import numpy as np

def find_files(indir, switch = False):
    """
    read all files in a directory and return a list of file paths
    If you want to search files under subdirectory change "switch" to True.

    Args
        indir: string
            input (or top) directory
        extension: string
            file extension (.ext)
        switch: boolean
            boolean parameter whether search subdirectory or not
            default is False
    Returns
        filapath: list
            a list of absolute file path
    """
    filepath = []
    for path, dirs, files in os.walk(indir):
        #print path, dirs
        for fname in files:
            if fname.endswith('X.csv'):
                filepath.append(os.path.join(path, fname))
        if switch = False:
            break
    return filepath

def parse_acquisition_data(path_string):
    """
    When reading an acqusition date from filepath, use this function while processing
        multiple metric files
    """
    regex = re.compile(r'\d{8}')
    yyyymmdd = regex.findall(path_string)

    return yyyymmdd

def update_plotmetric(infile, yyyymmdd):
    """
    read dataframe and additional columns

    Args
        dataframe: pandas dataframe
    Returns
        dataframe: updated dataframe with "AbsC" and "AbsR" columns
    """
    columns = ['Technology', 'Location', 'Field', 'Crop', 'EntityName', 'GrowthStage', \
               'Program', 'AbsR', 'AbsC', 'PlotBID', 'Latitude', 'Longitude', 'Metric', \
               'Value', 'FieldID', 'MetricVersion', 'MetricUnitOfMeasure', 'AcquisitionDate']

    # create empty dataframe
    empty_df = pd.DataFrame(columns = columns)

    # read plot metric data frame
    data_df = pd.read_csv(infile)

    # merge data frames
    updated_df = pd.concat([empty_df, data_df], ignore_index=True)

    # fill in fixed values
    updated_df['Technology'] = 'MAV'
    updated_df['Program'] = 'SD419'

    # obtain acquisition date from filepath
    yyyy = yyyymmdd[0:4]
    mm = yyyymmdd[4:6]
    dd = yyyymmdd[6:8]

    updated_df['AcquisitionDate'] = yyyy + '-' + mm + '-' + dd + 'T00:00:00-00:00'

    updated_df = updated_df[columns]

    #updated_df.to_csv(infile, index=False)
    return updated_df

if __name__ == "__main__":

    infile = '/Users/hojin.kim/pc-share/Biotech/Results_NERC_RCY2_X.csv'
    outdir = os.path.dirname(infile)

    # specify an acquistion date
    yyyymmdd = '20170709'

    # update metric file with adding columns
    updated_metric = update_plotmetric(infile, yyyymmdd)

    out_prefix = os.path.basename(infile).split('_')
    #yyyymmdd = parse_acquisition_data(infile)

    print (yyyymmdd)
    out_name = '{}_{}_{}_X_{}.csv'.format(out_prefix[0], out_prefix[1], out_prefix[2], ''.join(yyyymmdd))

    if not os.path.exists(outdir):
        os.makedirs(outdir)

    out_file = os.path.join(outdir, out_name)

    updated_metric.to_csv(out_file, index=False)
