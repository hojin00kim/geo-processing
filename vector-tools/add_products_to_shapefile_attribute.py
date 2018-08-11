"""
This is one of tools for validating metric results that were generated from MAV/UAV images.
used tk library for users who are not familiar with command line tools.

In order to check the spatial pattern, metrics need to join into plotgrid geometry and
update attribute table within the shapefile

"""

import os
import sys

import geopandas as gpd
from geopandas import GeoDataFrame
import fiona
import numpy as np
import pandas as pd

import tkinter.simpledialog as tksd
from tkinter import *
from tkinter.filedialog import askopenfilename


def csvfile_to_dataframe(infile, product):

    """
    read a csv files, select columns of interest and return a dataframe

    Args
        infile: string
            input filepath of a csv file
        product: product type that is going to add in the attribute table
            for ex. LAI, LAI_CV, or NDVI
    Returns
        metric_df: dataframe
    """

    metric = product

    # read a csv file and convert it to a data frame
    df = pd.read_csv(infile)

    # select columns that are necessary for joining tables
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
    read a ESRI shapefile and return a geo-dataframe

    Args
        infile: string
            input filepath of a shapefile
    Returns
        gdf: geo dataframe
    """
    gpd_data = gpd.GeoDataFrame.from_file(infile)

    # for checking CRS of the shapefile
    #crs = gdp_data.crs

    return gpd_data

def main(csv_file_path, shp_file_path, product):
    """
     Reads input csv and shapefile path and define product type
         and update shapefile with added product attributes

     Returns
         None
     """
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

    # Type product type
    product = tksd.askstring("Dialog (String)", "Enter product type in upper case :",
                                      parent=root)
    print(product)
    root.withdraw()


    main(csv_file_path, shp_file_path, product)

    button = Button (frame, text="Good-bye.", command=window.destroy)
    mainloop()
