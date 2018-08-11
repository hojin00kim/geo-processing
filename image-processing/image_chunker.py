import os, sys
from osgeo import gdal

"""
This is a tool to subset (or splitting) a large image with smaller tile size

"""
# specify input directory
imgdir = '/Users/hojin.kim/pc-share/image_chunker_test'
os.chdir(imgdir)

# specify input image filename
inputfile = '20170706_ILJED2_RGBN_Rad.tif'

# open image file and dump into a gdal object
dset = gdal.Open(inputfile)

# image width and height size
width = dset.RasterXSize
height = dset.RasterYSize

# print out image size
print (width, 'x', height)

# tilesize will be width x height
# width tile size
w_size = 500

# height tile size
h_size = 1000

# do chunk
for i in range(0, width, w_size):
    for j in range(0, height, h_size):
        w = min(i + w_size, width) - i
        h = min(j + h_size, height) - j
        gdaltranString = "gdal_translate -of GTIFF -srcwin "+ str(i) + ", " \
                            + str(j) + ", " + str(w) + ", " + str(h) + " " + inputfile \
                            + " " + 'Subset' + "_" + str(i) + "_" + str(j) + ".tif"
        os.system(gdaltranString)
