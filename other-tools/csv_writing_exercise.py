"""
A good practice tool for pandas dataframe and csv library

You can quickly exercise with
    1. reading a csv file
    2. converting it to a dataframe
    3. extracting values from a column (or columns)
    4. writing those values into a csv file
"""

import os

import pandas as pd
import csv

# specify file path
infile = '/Users/hojin.kim/pc-share/test-original.csv'

# load csv file to a dataframe
df = pd.read_csv(infile)

# slice dataframe with a specific metric
df = df[df.Metric == 'LAI']

# slice dataframe with a specific column
values = df['Value']

# cast the value to a list
values_list = values.tolist()

# This is just for practicing values to add 100 and restore to a list
added = []
for i in values_l:
    #print (("The '{}'th number is ".format(i)), i)
    add = i + 100
    added.append(add)

# specify output file name
outfile = os.path.join(os.path.dirname(infile), 'test-3.csv')

"""
You can write to a csv file in three ways
1. dataframe -> csv
2. csv writer
3. csv DictWriter
"""
# case 1: dataframe -> csv file
# df = pd.DataFrame({'Values': added})
# out_file = os.path.join(os.path.dirname(infile), 'test-csv.csv')
# df.to_csv(out_file, index = False)

# case 2: using csv writer
# with open(csvfile, "w") as output:
#     writer = csv.writer(output, lineterminator='\n')
#     for val in added:
#         writer.writerow([val])

# case 3: using csv DictWriter
with open(outfile, 'w') as csvfile:
    fieldnames = ['value']
    writer = csv.DictWriter(csvfile, delimiter=',', fieldnames=fieldnames)
    writer.writeheader()
    for row in added:
        writer.writerow({'value': row})
