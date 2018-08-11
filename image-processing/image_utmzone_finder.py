"""
Finding image UTM zone from geographic lat/lon coordinate system

"""
import gdal
import numpy as np

def load_band(fname):
    """
    read a raster file and put it into a gdal object

    Args
        fname: string
            input filepath

    Returns
        originX, originY: float
            x, y coordinates in floating point
    """
    #open input image
    input_ds = gdal.Open(fname, gdal.GA_ReadOnly)

    #print input_ds.RasterCount

    if input_ds is None:
        print ("Could not open " + fname)
        sys.exit(1)

    input_array = np.zeros((input_ds.RasterYSize, input_ds.RasterXSize, input_ds.RasterCount))

    for b in range(input_ds.RasterCount):
        band = input_ds.GetRasterBand(b + 1)
        input_array[:, :, b] = band.ReadAsArray().astype(np.uint16)

    # if input array has only one band
    #input_array = np.array(input_ds.GetRasterBand(1).ReadAsArray()).astype(np.uint16)

    # dimensions
    cols = input_ds.RasterXSize
    rows = input_ds.RasterYSize
    bands = input_ds.RasterCount
    geoT = input_ds.GetGeoTransform()
    proJ = input_ds.GetProjection()

    originX = geoT[0]
    originY = geoT[3]
    pixelWidth = geoT[1]
    pixelHeight = geoT[5]

    print (originX)
    print (originY)

    return originX, originY


def utm_getZone(longitude, latitude):
    """
    read lat/lon in decimal degree and obtain corresponding UTM utm_zone

    Args
        longitude, latitude: float
            latitude & longitude in decimal degree

    Returns
        utm_zone, is_north: integer, string
            utm zone id and if it is north of south in "N" or "S"

    """
    utm_zone = int(1+(longitude+180.0)/6.0)

    is_north = 0
    if (latitude < 0.0):
        is_north = "S";
    else:
        is_north = "N";

    return utm_zone, is_north


if __name__ == '__main__':

    fname = '/Users/hojin.kim/pc-share/test_latlon-2.tif'
    lon, lat = load_band(fname)[:2]
    utm_zone, north = utm_getZone(lon, lat)
    print (utm_zone, north)
