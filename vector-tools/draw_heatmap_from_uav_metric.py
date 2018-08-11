import geopandas as gpd
from geopandas import GeoDataFrame
import fiona
import os, sys
import pandas as pd
import numpy as np
import tkinter.simpledialog as tksd
from tkinter import *
from tkinter.filedialog import askopenfilename


def csvfile_to_dataframe(infile, product):

    metric = product
    # read a csv file and convert it to a data frame
    df = pd.read_csv(infile)

    # select columns with 'row', 'column', and 'LAI'
        #metric = product
    # read a csv file and convert it to a data frame
    df = pd.read_csv(infile)

    # select columns with 'row', 'column', and 'LAI'
    df = df[['Location', 'Field', 'Crop', 'GrowthStage',
             'AbsR', 'AbsC', 'Longitude', 'Latitude', 'EntityName',
             'Metric', 'Value']]

    # change the column name to match uav data
    df.columns = ['Location', 'Field', 'Crop', 'GrowthStage',
                  'Range', 'Column', 'Longitude', 'Latitude', 'EntityName',
                  'Metric', metric]

    # slice the data frame for designated product row;'LAI' only
    metric_df = df[df.Metric == metric]

    # drop "Metric" column
    metric_df = metric_df.drop('Metric', 1)

    return metric_df


def shapefile_to_geodataframe(infile):
    """
    Convert shapefile into geopandas dataframe
    """
    gpd_data = gpd.GeoDataFrame.from_file(infile)
    #crs = gdp_data.crs

    return gpd_data

def main(csv_file_path, shp_file_path, product):

    csv_file_dir = os.path.dirname(csv_file_path)
    shp_file_dir = os.path.dirname(shp_file_path)

    csv_file_name = os.path.basename(csv_file_path)
    shp_file_name = os.path.basename(shp_file_path)

    # covert input shapefile to dataframe
    grid_df = gpd.GeoDataFrame.from_file(shp_file_path)
    crs = grid_df.crs

    product_df = csvfile_to_dataframe(csv_file_path, product)

    # merte shapefile and plotmetric dataframe
    df = grid_df.merge(product_df, on=['Range', 'Column'])

    out_name = (csv_file_name.split('.')[0]) + '_' + product + '.shp'

    out_file_path = os.path.join(csv_file_dir, out_name)

    df.to_file(out_file_path, driver='ESRI Shapefile')


if __name__=="__main__":

    root = Tk()
    root.withdraw()

    csv_file_path = askopenfilename(filetypes=[('.csvfiles', '.csv')],
                                        title='Select csv file')
    print(csv_file_path)
    #csv_file_dir = os.path.dirname(csv_file_path)

    shp_file_path = askopenfilename(filetypes=[('.shpfiles', '.shp')],
                                        title='Select shp file')
    print(shp_file_path)
    #shape_file_dir = os.path.dirname(shape_file_path)
    root.withdraw()

    # Type acquistion date
    product = tksd.askstring("Dialog (String)", "Enter product type in upper case :",
                                      parent=root)
    print(product)
    root.withdraw()

    main(csv_file_path, shp_file_path, product)
    
