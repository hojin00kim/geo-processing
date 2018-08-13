
import pandas as pd
import numpy as np
import os, sys, shutil
from decimal import Decimal


def csv_to_dataframe(infile, product):
    """np.seterr(divide='ignore')
    Clean out the original csv file and and retrieve LAI rows
        and save it to a dataframe
    """
    metric = product
    # read a csv file and convert it to a data frame
    df = pd.read_csv(infile)

    # select columns with 'row', 'column', and 'LAI'
    metric_df = df[['Location', 'Field', 'AbsR', 'AbsC', 'Metric', 'Value']]

    # slice the data frame for 'LAI' row only
    index_df = metric_df[metric_df.Metric == metric]

    return index_df


def compute_levels(index_df):
    # create a list of the LAI values
    val_list = index_df['Value'].tolist()

    # find min and max value from the list
    maxval = max(val_list)
    minval = min(val_list)
    
    print 'max LAI value is :', maxval
    print 'min LAI value is :', minval

    # compute an interval, it gives six different levels
    # if you want to increase number of image files to check
    # change the step
    np.seterr(divide='ignore', invalid='ignore')
    step = 10
    interval = (maxval - minval) / step
    #print interval
    
    # create lai vlaues with several different level
    # step value will handle the number of levels
    levels = np.arange(minval, maxval + 1, interval).tolist()
    
    # rounded the output value with two decimal places
    rounded_levels = [round(elem, 2) for elem in levels]
    
    return val_list, rounded_levels

def find_nearest(array, value):
    """
    Function to find closest number with given values
        from an array
    """
    idx = (np.abs(array-value)).argmin()
    return array[idx]


def find_closest_index(val_list, rounded_levels):
    
    # convert the list of lai values into an array
    dataarray = np.asarray(val_list)

    # find closest numbers with the levels
    findings = []
    for val in rounded_levels:
        n = round(find_nearest(dataarray, val), 2)
        findings.append(n)
    
    return findings

def create_output_df(findings, index_df):
    # create data frame that subsets rows with matching lai values
    
    #index_df = clean_csv_table(infile, product)
    
    dfs = []
    for vals in findings:
        row = index_df[index_df.Value == vals]
        dfs.append(row)
        sum_df = pd.concat(dfs)
    
    return sum_df

def make_image_filename(validation_df):
    
    df = validation_df
    
    image_names = []
    for index, row in df.iterrows():
        
        rang = str(row['AbsR'])
        column = str(row['AbsC'])
        rgb_name = 'C' + column + '_' + 'R' + rang + '_RGB.tif'
        mask_name = 'C' + column + '_' + 'R' + rang + '_mask.tif'
        image_names.append(rgb_name)
        image_names.append(mask_name)
            
    return image_names

def copy_image_files(imgdir, outdir, validation_df):
    """
    Function to copy image files; RGB and masked (LAI) into a new folder 
        for analysis
    """
    
    src_dir = imgdir
    dst_dir = outdir
    image_list = make_image_filename(validation_df)
    
    # source directory and files
    source_images = []
    for src_name in image_list:
        in_path = os.path.join(src_dir, src_name)
        #print in_path
        source_images.append(in_path)
        
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
        
    for f in source_images:
        #print f
        shutil.copy(f, dst_dir)

def convert_xlsx_to_csv(infile):
    
    data_xls = pd.read_excel(infile, 'Sheet1', index_col=None)
    temp_csv = (os.path.basename(infile)).split('.')[0] + '.csv'
    data_xls.to_csv(temp_csv, encoding='utf-8')

    
def main(root_dir, infile, product):
    """
    This is a wrapper function to compute whole process
    """
    os.chdir(root_dir)
    
    df = csv_to_dataframe(infile, product)
    val_list, levels = compute_levels(df)
    findings = find_closest_index(val_list, levels)
    
    df_int = create_output_df(findings, df)
    
    # save datafrme with unique values (dropping duplicate)
    df_valid = df_int.drop_duplicates(subset = ['Value'])
    
    # save validation information to an excel file
    outstr = infile.split('.')[0]
    outname = outstr + '_validation.xlsx'
    df_valid.to_excel(outname)

    # copy extracted image files for validation into a folder
    plot_image_dir = os.path.join(root_dir, 'PlotImages')
    val_image_dir = os.path.join(root_dir, 'ValImages')
    
    if not os.path.exists(val_image_dir):
        os.makedirs(val_image_dir)
        
    copy_image_files(plot_image_dir, val_image_dir, df_valid)
    

if __name__=='__main__':
    
    filepath = sys.argv[1]
    
    print (filepath)

    root_dir, metric_file = os.path.split(filepath)
    os.chdir(indir)
    product = 'LAI'
    
    main(root_dir, metric_file, product)


