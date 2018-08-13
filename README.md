
# Geospatial-Toolbox

## Introduction
This is a personal repo for answering various questions that I have faced while working on image (raster) and vector data processing and analysis. Most of the tools are written by Python preferably version 3 (>= 3.5). 

These tools are distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Library General Public License for more details.  

Author: Hojin Kim  

##### image-processing
|file                           | Description   |
|:------------------------------|:--------------|
|raster_shift.py                | shift (affine transformation) a raster file in x/y direction with a user defined pixel counts in geographic coordinate systems |
|clip_raster_to_polygon.py      | clip a raster file to polygon either a single feature or  multiple features from the attribute table |
|rgb_image_rotator.py | rotate raster file (rgb geotiff format) to an arbitrary angle |
|update_raster_geotiff_header.py | update imagery geotiff header based on twf file |
|image_utmzone_finder.py | find matching utm zone from image with geographic coordinate system |
|image_chunker.py | chunk imagery data by user defined window size |
|quad_blob_estimation.py | estimate percentage of blob area from each quad section | 

##### vector-tools
|file                           | Description   |
|:------------------------------|:--------------|
|parse_dms_to_decimaldegree.py  | read degree/minute/second format lat/lon and convert to decimal degree |
|modify_shapefile_attributetable.py | read a shapefile and update attribute table with adding/subtracting/modifying, etc |
|obtaining_polygon_centroid.py | read a polygon shapefile that contains a single (or multiple) features and save centroids to a shapefile |
|add_products_to_shapefile_attribute.py| joining tables between shapefile and metric file and add an attribute to the shapefile for helping to delineate heatmap|
|shapefile_splitter.py | splitting a shapefile by using one of it's attribute |   


##### others-tools
|file                           | Description   |
|:------------------------------|:--------------|
|csv_writing_exercise.py| exercise three ways of writing a csv file using values extracted from a pandas dataframe |
|dataframe_column_sorting.py | if you want to sort multiple columns A-Z, A-Z such as an excel tool |
|random_extraction_by_group.py | extract random samples from column values after groupby |
|plotmetric_csv_to_json_upload_to_s3.py| metric uploading tool especially for Breeding UAV metrics |
