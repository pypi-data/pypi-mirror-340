import os
import numpy as np
import xarray as xr
from osgeo import gdal, gdal_array
from phenology.utils import Aggregate

# Enable exception handling
gdal.UseExceptions()

def read_geotiff(file_path):
    """
    Read data from a GeoTIFF file.

    Parameters:
        file_path (str): Path to the GeoTIFF file.

    Returns:
        tuple: (data, geotrans, proj)
            - data (np.ndarray): Data array read from the file. For multi-band images, the shape is (bands, rows, cols).
            - geotrans (list): Affine transformation parameters in the form 
                               [top left x, pixel width, rotation, top left y, rotation, -pixel height].
            - proj (str): Projection information.
            
    In case of an error, prints an error message and returns (None, None, None).
    """
    try:
        dataset = gdal.Open(file_path)  # Open the GeoTIFF file
        if dataset is None:
            raise RuntimeError(f"Failed to open GeoTIFF file: {file_path}")

        data = dataset.ReadAsArray()  # Read the data array
        geotrans = dataset.GetGeoTransform()  # Get affine transformation parameters
        proj = dataset.GetProjection()  # Get projection information

        return data, list(geotrans), proj

    except Exception as e:
        print(f"Error in reading GeoTIFF file: {str(e)}")
        return None, None, None

    finally:
        if dataset is not None:
            dataset = None  # Release resources


def write_geotiff(output_path, data, geotrans, proj, options=["TILED=YES", "COMPRESS=LZW"]):
    """
    Write data to a GeoTIFF file.

    Parameters:
        output_path (str): Path where the GeoTIFF file will be saved.
        data (np.ndarray): Data array to write. For multi-band images, the shape should be (bands, rows, cols).
                           If a 2D array is provided, it will be converted to a 3D array with one band.
        geotrans (tuple): Affine transformation parameters in the form 
                          (top left x, pixel width, rotation, top left y, rotation, -pixel height).
        proj (str): Projection information.
        options (list): GDAL creation options (e.g., ["TILED=YES", "COMPRESS=LZW"]). Defaults to tiled and LZW compression.

    Returns:
        None

    The function creates a GeoTIFF file at the specified output path using the provided data,
    geotransformation, projection, and options.
    """
    try:
        # Convert numpy dtype to GDAL type code
        datatype = gdal_array.NumericTypeCodeToGDALTypeCode(data.dtype) 
        driver = gdal.GetDriverByName("GTiff")  # Get the GeoTIFF driver
        if len(data.shape) == 2:
            data = np.array([data])             # Convert 2D data to a 3D array with one band
        bands, rows, cols = data.shape          # Get the number of bands, rows, and columns
         
        if options is None:
            options = []  # 默认为空列表
        dataset = driver.Create(output_path, cols, rows, bands, datatype, options=options)
        if dataset is None:
            raise RuntimeError("Failed to create output GeoTIFF file.")

        dataset.SetGeoTransform(geotrans)   # Set affine transformation
        dataset.SetProjection(proj)         # Set projection
        for band_index, band_data in enumerate(data, start=1):
            dataset.GetRasterBand(band_index).WriteArray(band_data)  # Write each band

        dataset.FlushCache()  # Write to disk

    except Exception as e:
        print(f"Error in writing GeoTIFF file: {str(e)}")

    finally:
        if dataset is not None:
            dataset = None  # Close the file



def complement_raster(input_file, output_file=None, exc_geos=[90, -90, -180, 180]):
    """
    Pad a raster from a GeoTIFF to a desired geographic extent.

    Reads the GeoTIFF from `input_file`, pads missing areas with NaN so that the 
    raster matches the desired extent (exc_geos = [max_lat, min_lat, min_lon, max_lon]), 
    and either writes the result to `output_file` or returns the padded data.

    Parameters:
        input_file (str): Path to the input GeoTIFF.
        output_file (str, optional): Output file path. If None, the function returns (data, geos, proj).
        exc_geos (list): Desired geographic bounds [max_lat, min_lat, min_lon, max_lon]. Default is [90, -90, -180, 180].
    """
    data, geos, proj = read_geotiff(input_file)
    data = data.astype(np.float32)
    rows, cols = data.shape
    x_min = geos[0]
    x_res = geos[1]
    y_max = geos[3]
    y_res = geos[5]
    x_max = x_min + x_res * cols
    y_min = y_max + y_res * rows

    miss_l = round(abs((exc_geos[2] - x_min)/x_res))
    miss_r = round(abs((exc_geos[3] - x_max)/x_res))
    miss_t = round(abs((exc_geos[0] - y_max)/y_res))
    miss_b = round(abs((exc_geos[1] - y_min)/y_res))
    
    data = np.pad(data, ((miss_t, miss_b), (miss_l, miss_r)), 'constant', constant_values=np.nan)
    geos[0] = exc_geos[2] # update min_lon
    geos[3] = exc_geos[0] # update max_lat

    if output_file:
        write_geotiff(output_file, data, geos, proj)
    
    else:
        return data, geos, proj
    
    

def nanmode_tiff(input_file, output_file=None, exc_shape=None, val_range=(1, 20)):
    """
    Replace out-of-range values with NaN, aggregate the raster to a new shape, and compute the mode.

    Reads the GeoTIFF from `input_file`, sets values outside `val_range` to NaN, adjusts the geotransform 
    for the desired output shape (`exc_shape`), aggregates the data using mode (via the Aggregate class), and 
    either writes the result to `output_file` or returns it.

    Parameters:
        input_file (str): Path to the input GeoTIFF.
        output_file (str, optional): Output file path. If None, the function returns (res, geos, proj).
        exc_shape (tuple): Desired output shape (rows, cols) for aggregation.
        val_range (tuple): Valid value range (min, max). Values outside this range are set to NaN.
    """
    data, geos, proj = read_geotiff(input_file)
    data[(data < val_range[0]) | (data > val_range[1])] = np.nan
    geos[1] = geos[1]*data.shape[0]/exc_shape[0]
    geos[5] = geos[5]*data.shape[1]/exc_shape[1]
    res = Aggregate(data, exc_shape).mode()
    if output_file:
        write_geotiff(output_file, res, geos, proj)
    else:
        return res, geos, proj
    
    

def arr2tiff(output_file, data:np.ndarray, geotrans=(90, -90, -180, 180), proj='EPSG:4326', region='global'):
    """
    Convert a NumPy array (2D or 3D) to a GeoTIFF file.

    Parameters:
        output_file (str): Full path (folder and file name) for the output GeoTIFF.
        data (np.ndarray): 2D or 3D array containing the data to be written.
                           For a 2D array, it is assumed that the rows represent latitudes (from high to low)
                           and columns represent longitudes.
                           For a 3D array, the last two dimensions correspond to spatial dimensions (lat, lon)
                           and the first dimension represents bands.
        geotrans (tuple): Geographic bounds specified as (max_lat, min_lat, min_lon, max_lon).
                          Defaults to global bounds (90, -90, -180, 180).
        proj (str): Projection string (e.g., 'EPSG:4326'). Defaults to 'EPSG:4326'.
        region (str): Region identifier. If set to 'nh30', geotrans is overridden to (90, 30, -180, 180).

    Returns:
        None

    The function calculates the pixel resolution based on the data dimensions and geographic bounds,
    constructs a geotransform tuple (with top-left coordinate, pixel size, and no rotation),
    and writes the GeoTIFF file using an external function write_geotiff().
    """
    os.makedirs(os.path.dirname(output_file), exist_ok=True) # Create the output directory if it doesn't exist
    if data.ndim >3:
        raise ValueError("Data array must be 2D or 3D.")
    
    if region == 'nh30':
        geotrans = (90, 30, -180, 180)
        
    rows, cols = data.shape[-2:]
    max_y, min_y, min_x, max_x = geotrans
    res_x = (max_x - min_x)/cols
    res_y = (max_y - min_y)/rows
    new_geotrans = (min_x, res_x, 0, max_y, 0, -res_y)
    write_geotiff(output_file, data, new_geotrans, proj)



def xarr2tiff(output_file, ds:xr.Dataset, var_names=[], lat_name='lat', lon_name='lon', proj='EPSG:4326'):
    """
    Export variable(s) from an xarray.Dataset to GeoTIFF file(s).

    Parameters:
        output_file (str): Full output file path (folder and file name) for the GeoTIFF.
                           If multiple variables are exported, each file will have the variable name appended.
        ds (xr.Dataset): xarray.Dataset containing the data.
        var_names (list): List of variable names to export. If empty, all data variables will be exported.
        lat_name (str): Name of the latitude coordinate in the dataset. Defaults to 'lat'.
        lon_name (str): Name of the longitude coordinate in the dataset. Defaults to 'lon'.
        proj (str): Projection string (e.g., 'EPSG:4326'). Defaults to 'EPSG:4326'.

    Returns:
        None

    The function extracts latitude and longitude values to define geographic bounds, ensures the output directory exists,
    and exports each variable as a GeoTIFF using the arr2tif function. Both 2D and 3D arrays are supported.
    """
    lats = ds[lat_name].values
    lons = ds[lon_name].values
    lat_start, lat_end = lats[0], lats[-1]
    lon_start, lon_end = lons[0], lons[-1]
    geotrans = (lat_start, lat_end, lon_start, lon_end)
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    if len(var_names) == 0:
        var_names = list(ds.data_vars)

    if len(var_names) == 1:
        data = ds[var_names[0]].values.squeeze()
        arr2tiff(output_file, data, geotrans, proj)

    else:
        for var in var_names:
            output_file_var = output_file.replace('.tif', f'_{var}.tif')
            data_var = ds[var].values.squeeze()
            arr2tiff(output_file_var, data_var, geotrans, proj)
            
            
            