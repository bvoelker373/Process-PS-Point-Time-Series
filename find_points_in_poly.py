"""ArcPy script to find points within polygons, and join their attribute tables"""

# Import system modules
import arcpy
import os

# Overwrite existing output.
arcpy.env.overwriteOutput = True

# Create intermediate data directory if it doesn't exist.
directory = "data_deprecated"
try:
    os.mkdir(directory)
except: 
    pass

# Create output directory if it doesn't exist.
directory = "out"
try:
    os.mkdir(directory)
except: 
    pass

# Absolute directory of workspace for ArcGIS.
workspace = r'C:\Users\Brandon\Documents\persistent_scatter\data'

# Initial parameters.
XY_table = r"ID_LAT_LON.csv"
polygons = r"C:\Users\Brandon\Documents\persistent_scatter\data\OR_landslides_corr_ZS.shp"

spatial_ref = arcpy.Describe(polygons).spatialReference
transformations = arcpy.ListTransformations("WGS 1984", spatial_ref)

# long_filed = LONG

try:
    # Set the current workspace (to avoid having to specify the full path to the feature classes each time)
    arcpy.env.workspace = workspace
    
    pts = arcpy.management.XYTableToPoint(XY_table, "ID_LAT_LON.shp",
                                          "LON", "LAT",
                                          "#", "#")
    print('XY Table Imported as Points')
    
    pts_proj = arcpy.management.Project("ID_LAT_LON.shp", "ID_LAT_LON_proj.shp",
                                        spatial_ref, transformations[0],
                                        "#", "#",
                                        "#", "#")
    print('Points Projected')
    
    
    
    
    print('Points Clipped to Polygons')
    
    
    print('Polygons Containing Points Selected')
    
    
    print('Points Spatially Joined to Polygons')
    
            
except arcpy.ExecuteError:
    # If any error occurred when running the tool, print the messages
    print(arcpy.GetMessages())
    
except Exception as ex:
    print(ex.args[0])