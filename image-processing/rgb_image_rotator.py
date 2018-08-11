"""
This is a tool for rotating multiband raster file in an arbitrary angle
"""

import os
import gdal
import numpy as np


def find_files(indir, switch = False):
    """
    read all files in a directory and return a list of file paths
    If you want to search files under subdirectory change "switch" to True.

    Args
        indir: string
            input (or top) directory
        switch: boolean
            boolean parameter whether search subdirectory or not
            default is False
    Returns
        filapath: list
            a list of absolute file path
    """

    filepath = []
    for path, dirs, files in os.walk(indir):
        for fname in files:
            if fname.endswith('.tif'):
                filepath.append(os.path.join(path, fname))

        if switch == False:
            break
    return filepath

def load_band(fname):
    """
    Load raster file and extract geotiff header information using gdal

    Args
        fname: string
            input file name
    Returns
        gdal object parameters

    """
    # open input image
    input_ds = gdal.Open(fname, gdal.GA_ReadOnly)

    #print (input_ds.RasterCount)

    if input_ds is None:
        print ("Could not open " + fname)
        sys.exit(1)

    input_array = np.zeros((input_ds.RasterYSize, input_ds.RasterXSize, input_ds.RasterCount))

    for b in range(input_ds.RasterCount):
        band = input_ds.GetRasterBand(b + 1)
        input_array[:, :, b] = band.ReadAsArray().astype(np.uint8)

    cols = input_ds.RasterXSize
    rows = input_ds.RasterYSize
    bands = input_ds.RasterCount
    geoT = input_ds.GetGeoTransform()
    proJ = input_ds.GetProjection()
    originX = geoT[0]
    originY = geoT[3]
    pixelWidth = geoT[1]
    pixelHeight = geoT[5]

    return input_array, cols, rows, bands, geoT, proJ, originX, originY, pixelWidth, pixelHeight

def compute_rotation_parameters(infile, angle):

    """
    Load raster file and extract geotiff header information using gdal

    Args
        infile: string
            input file name
        angle: float
            arbitrary angle with image rotated
    Returns
        tuple: geotranformation parameters

    """
    cols, rows, bands, geoT, proJ, originX, originY, pixelWidth, pixelHeight = load_band(infile)[1:]

    # performa rotation using the angle, if you want to rotate the image around the center
    # of the origin (originX, originY), add "cellSizeX / 2" to GeoTransform[0], and subtract
    # from GeoTransform[3]

    rotation = np.radians(angle)

    GeoTransform = list(geoT)
    GeoTransform[0] = originX;
    GeoTransform[1] = np.cos(rotation) * pixelWidth;
    GeoTransform[2] = -np.sin(rotation) * pixelWidth;
    GeoTransform[3] = originY;
    GeoTransform[4] = np.sin(rotation) * pixelHeight;
    GeoTransform[5] = np.cos(rotation) * pixelHeight;

    return tuple(GeoTransform)

def process_rotation(indir, outdir, angle):
    """
    Args
        indir: string
            input (or top) directory
    Returns
        None: rotated image will be saved to a folder
    """

    # obtain all files to be rotated

    files = find_files(indir)

    for f in files:

        array, cols, rows, bands, geoT, proJ, originX, originY, pixelWidth, pixelHeight  = load_band(f)
        post_geoT = compute_rotation_parameters(f, angle)

        print ("Rotating file :", f)

        # write output to a file
        filebase = os.path.basename(f).split('.')[0] + '_rot.tif'
        outfile = os.path.join(outdir, filebase)

        driver = gdal.GetDriverByName("GTiff")
        out_array = driver.Create(outfile, cols, rows, 3, gdal.GDT_Byte)
        out_array.SetGeoTransform(post_geoT)
        out_array.SetProjection(proJ)
        out_array.GetRasterBand(1).WriteArray(array[:, :, 0])
        out_array.GetRasterBand(2).WriteArray(array[:, :, 1])
        out_array.GetRasterBand(3).WriteArray(array[:, :, 2])
        out_array.FlushCache()
        out_array = None

if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(description = "RGB image rotation")
    parser.add_argument("-i", "--indir", help = "Input directory", required = True)
    parser.add_argument("-o", "--outdir", help = "Output directory", required = True)
    parser.add_argument("-a", "--angle", type = float, help = "an angle of rotation")
    args = parser.parse_args()

    indir = args.indir
    outdir = args.outdir
    angle = args.angle

    if not os.path.exists(indir):
        print("Path {} does not exist".format(indir))

    process_rotation(indir, outdir, angle)
