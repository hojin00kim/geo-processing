"""
This little tool does shift (affine transformation) a raster file in x/y direction
with a user defined pixel counts in geographic coordinate systems.

Number of pixels in x/y direction need to be provided.

Usage: co-registering imagery data that were acquired two different times.
       band-band registration
"""

import os
import sys

import gdal


def raster_shift(infile, x_pixels, y_pixels):
    """
    read a raster file and number of pixels that user provided
    and shift the raster in x/y direction

    Args
        infile: string
            a raster file in geotiff format
        x_pixels: int or float
            nuber of pixels in x (longitude) direction
        y_pixels: int or float
            nuber of pixels in y (latitude) direction
    Returns
        None
    """

    ds = gdal.Open(infile, gdal.GA_Update)

    # get the geotransform as a tuple of 6, below are the information of each parameters
    # GeoTransform[0] /* upper left x */
    # GeoTransform[1] /* west-east pixel resolution */
    # GeoTransform[2] /* 0 */
    # GeoTransform[3] /* upper left y */
    # GeoTransform[4] /* 0 */
    # GeoTransform[5] /* north-south pixel resolution (negative value) */

    gt = ds.GetGeoTransform()
    # unpack geotransform into variables
    x_ul, x_resolution, dx_dy, y_ul, dy_dx, y_resolution = gt

    # compute shift of # pixel RIGHT in X direction (+)
    shift_x = x_pixels * x_resolution

    # compute shift of # pixels UP in Y direction (-2), shift down (+)
    # y_res likely negative, because Y decreases with increasing Y index
    shift_y = y_pixels * y_resolution

    # make new geotransform
    gt_update = (x_ul + shift_x, x_resolution, dx_dy, y_ul + shift_y, dy_dx, y_resolution)

    # assign new geotransform to raster
    ds.SetGeoTransform(gt_update)

    # ensure changes are committed
    ds.FlushCache()
    ds = None

if __name__ == "__main__":

    # open dataset with update permission
    indir = r'C:\Users\hkim8\Project\2017_Data_Processing\MAV\KSHGD'
    os.chdir(indir)

    infile = '20170820_KSHGD_RGBN_Rad.tif'

    # pixel number can be an integer or floating point
    x_pixels = 2
    y_pixels = 2

    raster_shift(infile, x_pixels, y_pixels)
