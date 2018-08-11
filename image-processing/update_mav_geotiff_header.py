"""
Updating geotiff image geotiff header

In 2017, there are lot of MAV imagery has missing geotiff header information
that resulted in failure to injest into image processing pipeline.

It turned out that twf file was provided but image itself did not contain
georeference information.

This scrip does update geotiff header based on information provided from twf file.
"""

import os

import gdal
import osr
import gdal

def update_uav_crs(infile, metafile):
        """
        read a geotiff file and metafile and update geotiff header of the image

        Args
            infile: string
                input file path
            metafile: string
                meta file path
        Returns
            None
        """
    # read image to get array size
    input_ds = gdal.Open(imgfile, gdal.GA_Update)

    cols = input_ds.RasterXSize
    rows = input_ds.RasterYSize

    with open(twffile, 'r') as twffile:
        data = twffile.read().splitlines()

    x0 = float(data[4].strip())  # xmin
    y0 = float(data[5].strip())  # ymax
    gridWidth = float(data[0].strip())  # in decimal degree
    gridHeight = float(data[3].strip())  # in decimal degree
    xe = float(x0 + (abs(gridWidth) * cols))  # xmax
    ye = float(y0 - (abs(gridHeight) * rows))  # ymin

    # make new geotransform
    gt_update = (x0, gridWidth, 0, y0, 0, gridHeight)

    # update new geotransform to raster
    input_ds.SetGeoTransform(gt_update)

    # ensure changes are committed
    input_ds.FlushCache()
    input_ds = None

if __name__ == '__main__':


    import argparse

    parser = argparse.ArgumentParser(description = "Geotiff header update")
    parser.add_argument("-i", "--infile", help = "Input file path", required = True)
    parser.add_argument("-m", "--metafile", help = "Metafile path", required = True)
    args = parser.parse_args()

    infile = args.infile
    metafile = args.metafile

    if not os.path.exists(infile):
        print("Path {} does not exist".format(infile))

    update_uav_crs(infile, metafile)
