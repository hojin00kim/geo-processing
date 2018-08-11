"""
This is a dataframe sorting tool in order. When working with metric files from MAV
 or UAV, you will probably need to sort range and column id for quick metric value
 evaluation.

There is a short description below and enjoy the tool.
"""

import os
import sys
import pandas as pd
import numpy as np

from decimal import Decimal

def clean_csv_table(infile):
    """
    Read csv file, put into a dataframe and do some clean up

    :param infile: csv fiel - string
    :return: a dataframe
    """
    # read a csv file and convert it to a data frame
    df = pd.read_csv(infile)

    # select necessary columns for data processing
    metric_df = df[['Column', 'FieldName', 'LDR', 'Range']]

    # change column order to easy manipulation
    metric_df = metric_df[['FieldName', 'Column', 'Range', 'LDR']]

    data_df = metric_df

    return data_df

def reordering_dataframe_columns(df):
    """
    Usage is as follows;
    pandas dataframe method (sort_values) will re-arrange range and column numbers in order.
    You have a dataframe with three columns and multiple observations;

    df:

    Range    Column   Measurement
    3        2        0.01
    2        3        0.23
    3        1        0.31
    1        2        0.56
    2        2        0.66
    2        1        0.55
    1        3        0.55
    3        3        0.8
    1        1        0.67

    and re-order it to

    Range    Column   Measurement
    1        1        0.67
    1        2        0.56
    1        3        0.55
    2        1        0.55
    2        2        0.66
    2        3        0.23
    3        1        0.31
    3        2        0.01
    3        3        0.8

    Parameters in the "sort_values" method determines what column sort first, and next.
    If you want to group 'range' and sort 'column' such as above example,

    ordered_df = indf.sort_values(['Range', 'Column']).reset_index()

    or if you want to group 'column' and sort 'range'

    ordered_df = indf.sort_values(['Column', 'Range']).reset_index()

    In order to make it descending order; max number first, give 'ascending' parameter as 'False'

    grpdf = df.sort_values(['Range', 'Column'], ascending=[False, False]).reset_index()

    """

    sorted_df = df.sort_values(['Range', 'Column']).reset_index()

    return sorted_df

if __name__ == "__main__":

    # specify directory
    indir = '/Users/hojin.kim/indir'
    os.chdir(indir)

    # input file is the resulting csv file from uavimageproc
    infile = 'metric_results.csv'
    df = clean_csv_table(infile)
    sorted_df = reordering_dataframe_columns(df)
