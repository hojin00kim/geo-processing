"""
Tool to extract random sample from each group. When column values contain
 multiple groups and you need to select randome samples from each group
"""

import os
import random
import sys

from decimal import Decimal
import numpy as np
import pandas as pd

def read_csv_to_df(infile):

    # read a csv file and convert it to a data frame
    df = pd.read_csv(infile)

    # select necessary columns
    df = df[['Column', 'FieldName', 'LDR', 'Range', 'Sharpness']]

    # remove empty cells
    df.replace(r'\s+', np.nan, regex=True)

    # change the column name to match uav data
    df = df[['FieldName', 'Column', 'Range', 'LDR', 'Sharpness']]

    return df


def random_sample_multiple_group(df, size):
    """
        randome sample from dataframe after group by a "column", if group doesn't exist
        just use df.sample(n=x) or df.sample(frac = 0.1)

    """

    # define a size of randome sample from each group
    if size > 1:

        col_name = 'LDR'
        size = size
        replace = True

        fn = lambda obj: obj.loc[np.random.choice(obj.index, size, replace), :]
        sampled_df = df.groupby(col_name, as_index=False).apply(fn)

    else:

        n = size * 10
        sampled_df = df.sample(n = n)

    # if you want to extract just one sample
    #yield_df.groupby('LDSR_CORBNE').apply(lambda x: x.iloc[np.random.choice(range(0, len(x)))])

    return sampled_df


if __name__ == "__main__":

    # specify directory
    indir = '/Users/hojin.kim/test'
    os.chdir(indir)

    # input file is the resulting csv file from uavimageproc
    infile = 'metric.csv'
    data_df = read_csv_to_df(infile)
    size = 1
    training_df = random_sample_multiple_group(data_df, size)

    # save training_df into a csv file
    training_df.to_csv('training_data.csv')
