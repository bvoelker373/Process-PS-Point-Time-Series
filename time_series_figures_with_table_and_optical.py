import os
import pandas as pd
import geopandas as gpd
import contextily as ctx
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib_scalebar.scalebar import ScaleBar
plt.ioff()

directory = "plots"
try:
    os.mkdir(directory)
except: 
    pass

data = pd.read_csv('merged.csv')

# Prepare the 3 inputs to the plot:
#########################################
#            Optical Imagery            #
#########################################
landslide_gdf = gpd.read_file('or_ls_dissolve.shp')

# Extract the lat/long data to a geodataframe.
coords = data[['Point_ID', 'LAT_x', 'LON_x']]
points_gdf = gpd.GeoDataFrame(
                    coords,
                    geometry = gpd.points_from_xy(coords.LON_x, coords.LAT_x)
                    ).set_crs("EPSG:4326")

# Project points to be in same coordinate system as landslides.
points_gdf_proj = points_gdf.to_crs(landslide_gdf.crs)

#########################################
#               Timeseries              #
#########################################
timeseries = data.filter(regex='20')
seperator = '_'

# Remove suffix from dates (e.g. 20171201_VV_25 --> 20171201).
timeseries.columns = timeseries.columns.str.split(seperator, 1)
timeseries.columns = [date[0] for date in timeseries.columns]

# Format dates.
x = pd.DataFrame(timeseries.columns, columns = ['Time'])
x['Time'] = pd.to_datetime(x['Time'], format='%Y%m%d', errors='coerce')

#########################################
#              Data Table               #
#########################################
data_subset = data[['FAIL_TYPE', 'TYPE_MOVE', 'CONFIDENCE', 'AGE',
                    'SLOPE', 'FAIL_DEPTH', 'DEEP_SHAL','COHER', 'STDEV']] \
                    .rename(
                    {'FAIL_TYPE': 'Fail Type',
                    'TYPE_MOVE': 'Movement Type',
                    'CONFIDENCE': 'Confidence',
                    'AGE': 'Age',
                    'SLOPE': 'Slope',
                    'FAIL_DEPTH': 'Fail Depth',
                    'DEEP_SHAL': 'Depth Type',
                    'COHER': 'Coherence',
                    'STDEV': 'Standard Deviation'
                    },
                   axis='columns')


#########################################
#               Plotting                #
#########################################
for index, row in timeseries.iterrows():
    print('Plotting: ', index)
    
    fig = plt.figure()
    fig.set_size_inches(23, 12)
    fig.set_dpi(300)
    fig.suptitle("Point {}".format(data['Point_ID'][index]))
    
    
    ax1 = plt.subplot2grid((12,12), (0,0), colspan=6, rowspan = 6) # left
    ax2 = plt.subplot2grid((12,12), (0,6), colspan=6, rowspan = 6) # right
    ax3 = plt.subplot2grid((12,12), (6,0), rowspan = 3, colspan=12) # bottom 
    
    """ Smaller plot, but more white space
    ax1 = plt.subplot2grid((2,2), (0,0)) # left
    ax2 = plt.subplot2grid((2,2), (0,1)) # right
    ax3 = plt.subplot2grid((2,2), (1,0), colspan = 2) # bottom 
    """
    
    ###########################
    # Axis 1: Optical imagery
    # Bounding box of mapped point
    # Essentially the same as the lat/long of the point,
    #   but these will be buffered later to create the image bounds 
    minx, miny, maxx, maxy = points_gdf_proj.loc[[index]].geometry.total_bounds
    
    # Plot the data
    landslide_gdf.plot(
        ax = ax1,
        linestyle = '-.',
        edgecolor = 'orange',
        facecolor = 'None',
        label = 'Landslide'
        )
    points_gdf_proj.loc[[index],'geometry'].plot(
        ax = ax1,
        marker='.',
        color='red',
        label = 'PS Point'
        )
    
    # Center around the point,and set extent with buffer around the point
    buffer = 1000
    ax1.set_xlim(minx - buffer, maxx + buffer)
    ax1.set_ylim(miny - buffer, maxy + buffer)
    
    # Add scalebar and legend for plotted data.
    ax1.add_artist(ScaleBar(1))
    custom_symbols = [Line2D([0], [0], linestyle = '-.', color='orange', lw=1.5),
                      Line2D([0], [0], linestyle = 'None', marker='.', color='red', lw=4)]
    ax1.legend(custom_symbols, ['Landslides', 'PS Point'], loc = 'upper left')
    
    ctx.add_basemap(
        ax = ax1,
        source = ctx.providers.Esri.WorldImagery,
        crs = landslide_gdf.crs)
    
    ###########################
    # Axis 2: Timeseries
    # Scatter method causes an error with the datetime, so just use normal plot
    ax2.plot(x['Time'], row,
             marker='.', mec='black', markerfacecolor='black',
             linestyle='None', markersize = 4)
    
    ax2.set_xlabel("Date")
    ax2.set_ylabel("Displacement [mm?]")
    
    ###########################
    # Axis 3: Data table
    ax3.axis('off')
    ax3.axis('tight')
    table = ax3.table(cellText=data_subset.iloc[[index]].values,
                      colLabels=data_subset.columns,
                      loc='top', cellLoc = 'center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    
    
    fig.tight_layout()
    fig.subplots_adjust(bottom=0)
    plt.savefig('{}\{}_{}.png'.format(directory, data['Point_ID'][index], index), bbox_inches='tight', pad_inches=0.0)
    plt.close()
        
        
##############################################################################
# Reference Material

"""
https://stackoverflow.com/questions/49323439/plot-the-geometry-of-one-row-of-a-geodataframe
https://gis.stackexchange.com/questions/332624/geopandas-plot-two-layers-but-only-to-the-extent-of-the-smaller-one
https://stackoverflow.com/questions/32137396/how-do-i-plot-only-a-table-in-matplotlib
https://stackoverflow.com/questions/21285380/find-column-whose-name-contains-a-specific-string
https://stackoverflow.com/questions/55679401/remove-prefix-or-suffix-substring-from-column-headers-in-pandas/55679432
https://stackoverflow.com/questions/904746/how-to-remove-all-characters-after-a-specific-character-in-python
https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.table.html
https://stackoverflow.com/questions/30968405/how-to-use-gridspec-with-pandas-plot
https://matplotlib.org/stable/gallery/text_labels_and_annotations/custom_legends.html
"""
