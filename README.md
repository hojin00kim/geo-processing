
# Geospatial-Toolbox

## Introduction
This is a personal repo for answering various questions that I have faced while working on image (raster) and vector data processing and analysis. Most of the tools are written by Python preferably version 3 (>= 3.5). All folders will have basically two sub-folders, notebook and src that contain Python notebook (jupyter notebook) files; .ipynb in the notebook folder and .py in the src folder. If possible, please use python scripts instead of notebook files, since notebook files are mainly for testing functionality and intermediate development purpose.  

This library is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Library General Public License for more details.  

Author: Hojin Kim  


##### geo-processing
|file                           | Description   |
|:------------------------------|:--------------|
|parse_dms_to_decimaldegree.py  | read degree/minute/second format lat/lon and convert to decimal degree |
|modify_shapefile_attributetable.py | read a shapefile and update attribute table with adding/subtracting/modifying, etc |
|obtaining_polygon_centroid.py | read a polygon shapefile that contains a single (or multiple) features and save centroids to a shapefile |
|shapefile_splitter.py | splitting a shapefile by using one of it's attribute |   

##### image-processing
|file                           | Description   |
|:------------------------------|:--------------|
|raster_shift.py                | shift (affine transformation) a raster file in x/y direction with a user defined pixel counts in geographic coordinate systems |
|clip_raster_to_polygon.py      | clip a raster file to polygon either a single feature or  multiple features from the attribute table |
|rgb_image_rotator.py | rotate raster file (rgb geotiff format) to an arbitrary angle |
|update_mav_geotiff_header.py | update MAV imagery geotiff header based on twf file |
|image_utmzone_finder.py | find matching utm zone from image with geographic coordinate system |
|image_chunker.py | chunk imagery data by user defined window size |  

##### mav-uav
|file                           | Description   |
|:------------------------------|:--------------|
|extract_validation_data_image.py| Select plot images randomly and slice output csv for validation |
|plotmetric_csv_to_json_upload_to_s3.py| metric uploading tool especially for Breeding UAV metrics |
|add_products_to_shapefile_attribute.py| joining tables between shapefile and metric file and add an attribute to the shapefile for helping to delineate heatmap|
|mav_metric_updator_single.py| update a single MAV metric file |  

##### uav-processing
|file                           | Description   |
|:------------------------------|:--------------|
|canopycoverage.py| compute canopy coverage from UAV RGB images |
|uniformity.py| compute plot uniformity from UAV RGB images |
|raster_clipper.py| clip image to polygons for ingesting canopy coverage and uniformity computation|
|  |  |  


##### others
|file                           | Description   |
|:------------------------------|:--------------|
|csv_writing_exercise.py| exercise three ways of writing a csv file using values extracted from a pandas dataframe |
|mav_planning_updator.py | read master spreadsheet for MAV acquisition plan and update weekly acquistion plan for six different protocols |
|dataframe_column_sorting.py | if you want to sort multiple columns A-Z, A-Z such as an excel tool |
|random_extraction_by_group.py | extract random samples from column values after groupby |  
