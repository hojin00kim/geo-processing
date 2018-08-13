
# coding: utf-8

# In[20]:

import sys, getopt, os
import pandas as pd
import csv
import json
import re
import datetime
import shutil
import boto3

conversions = {'Technology': str, 'SoftwareVersion': float, 'VehicleID': str, 'Location': str,                'Field': str, 'Crop': str, 'EntityName': str, 'Entry': str, 'Rep': str,                'GrowthStage': str, 'PlotLength': float, 'AlleyLength': float, 'Season': str,                'Program': str, 'RowsPerPlot': int, 'PlotBID': str, 'AbsR': int, 'AbsC': int,                'Latitude': float, 'Longitude': float, 'Set': str, 'Metric': str, 'Value': float,                'MetricVersion': int, 'MetricUnitOfMeasure': str, 'RouteToFTS': int, 'RouteToDSW': int,                'FieldID': str
               }


def convert_fields(iterable):
    for item in iterable:
        for key in item.viewkeys() & conversions:
            sKey = key.strip()
            item[sKey] = conversions[key](item[key])
        yield item
        

def chunk_csv_file(infile, linesize):
    
    # extract file base for output name
    out_prefix = infile.split('.')[0]
    
    # count number of lines of input file
    with open(infile) as csvfile:
        reader = csv.DictReader(csvfile)
        row_count = sum(1 for row in reader)
        
    if row_count <= linesize:
        shutil.copy(infile, out_prefix + '_0.csv')
        
    else:
        for i, chunk in enumerate(pd.read_csv(infile, chunksize=linesize)):   # chunk size is number of lines
            chunk.to_csv(out_prefix + '_{}.csv'.format(i), index = False)


def find_files(path, pattern):
    """
    find chunked csv files with _xx.csv xx = sequence numbers
    """
    pattern = re.compile(pattern)
    
    files = []
    for f in os.listdir(path):
        if pattern.search(f):
            try:
                files.append(f)
            except OSError as exc:
                print exc
    return files


def delete_files(path, pattern):
    """
    delete chucked csv files when json conversion is completed
    """
    pattern = re.compile(pattern)
    for f in os.listdir(path):
        if pattern.search(f):
            try:
                os.remove(os.path.join(path, f))
            except OSError as exc:
                print exc
                
                
def read_csv_to_json_list(infile, json_file):
    """
    Function to read a csv file
    """
    
    csv_rows = []
    with open(infile) as csvfile:
        
        reader = csv.DictReader(csvfile)
        title = reader.fieldnames
        
        # compare key value and convert correct type in the csv format
        reader = convert_fields(reader)
        
        for row in reader:
            csv_rows.extend([{title[i]:row[title[i]] for i in range(len(title))}])
        
    return csv_rows


def write_json_string(data, json_file):
    """
    Convert csv file into json formats; 'dump' or 'pretty'
    
    """
    with open(json_file, "w") as f:
        
        metric = {'objectType':'PlotMetric', 'projectCode':'imageanalyticsprod', 'data': data}
        
        f.write(json.dumps(metric, sort_keys=False, indent=4, ensure_ascii=False))

def json_string_to_file(indir, pattern):
    
        # find csv files with _xx.csv
    csv_files = find_files(indir, pattern)
    
    for f in csv_files:
        
        out_json = f.split('.')[0] + '.json'
        obj = read_csv_to_json_list(f, out_json)

        write_json_string(obj, out_json)
    
    delete_files(indir, pattern)
    
        
def upload_jsonfiles_to_s3(indir, s3_folder):

    session = boto3.Session(profile_name = 'fielddrive') # change credential profile accordingly
    fd_s3_client = session.client('s3')

    uav_bucket = 'connect-bulk-upload-prod'

    for root, dirs, files in os.walk(indir):
        for fname in files:
            if fname.endswith('.json'):
                fd_s3_client.upload_file(os.path.join(root, fname), uav_bucket, s3_folder + fname)
    
    
if __name__ == "__main__":
    
    # below is an example of test environment
    
    indir = r'C:\Users\hkim8\Project\2017_Data_Processing\fielddrive_upload\TEST' # input directory
    os.chdir(indir)
    
    metric_file = 'ILSO_KSO3_V3_PlotBID_20170522_LAI_LAICV.csv' # input file name
    
    # chucnk csv file to pieces to avoid FD size limitation
    chunk_csv_file(metric_file, 3000)
    
    # define pattern for json writing
    pattern = r'LAICV_\d.*\.csv$'
    
    json_string_to_file(indir, pattern)
    
    # define s3 folder where the data will be uploaded
    s3_folder = 'IMAGEANALYTICSTEST/UAV/201605/ILSO-KSO3/20170522/' # don't forget to add "/" at the end of the path

    # upload files
    upload_jsonfiles_to_s3(indir, s3_folder)


# In[ ]:



