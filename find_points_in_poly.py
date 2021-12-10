"""ArcPy script to find points within polygons, and join their attribute tables.
Final attribute table is dumped to Excel file."""

# Import system modules
import arcpy

# Overwrite existing output.
arcpy.env.overwriteOutput = True

# Absolute directory of workspace for ArcGIS.
workspace = r'C:\Users\Brandon\Documents\persistent_scatter\data'

# Initial parameters.
XY_table = r"ID_LAT_LON.csv"
polygons = r"C:\Users\Brandon\Documents\persistent_scatter\data\OR_landslides_corr_ZS.shp"
out_path = r"C:\Users\Brandon\Documents\persistent_scatter"
spatial_ref = arcpy.Describe(polygons).spatialReference
transformations = arcpy.ListTransformations("WGS 1984", spatial_ref)


try:
    # Set the current workspace (to avoid having to specify the full path to the feature classes each time)
    arcpy.env.workspace = workspace
    
    pts = arcpy.management.XYTableToPoint(XY_table, "ID_LAT_LON.shp",
                                          "LON", "LAT",
                                          "#", "#")
    print('\nXY Table Imported as Points')
    
    pts_proj = arcpy.management.Project("ID_LAT_LON.shp", "ID_LAT_LON_proj.shp",
                                        spatial_ref, transformations[0],
                                        "#", "#",
                                        "#", "#")
    print('\nPoints Projected')
    
    
    clip = arcpy.analysis.Clip("ID_LAT_LON_proj.shp", polygons,
                               "ID_LAT_LON_proj_clip.shp", "#")
    print('\nPoints Clipped to Polygons')
    
    
    poly_containing_pts = arcpy.management.SelectLayerByLocation(
            polygons, "CONTAINS",
            "ID_LAT_LON_proj_clip.shp", "#",
            "#", "#")
    print('\nPolygons Containing Points Selected')
    
    # If features matched criteria, write them to a new feature class
    matchcount = int(arcpy.GetCount_management(poly_containing_pts)[0]) 
    if matchcount == 0:
        print('WARNING: No polygons contained any point features.')
    else:
        arcpy.CopyFeatures_management(poly_containing_pts,
                                      "OR_Landslides_Containing_PS_Points.shp")
        print('\nPolygons Containing Points Exported as New Shapefile')
    
    sJoin = arcpy.analysis.SpatialJoin(
            "ID_LAT_LON_proj_clip.shp",
            "OR_Landslides_Containing_PS_Points.shp",
            "OR_PS_Within_LS.shp",
            "JOIN_ONE_TO_MANY",
            "#", "#", "#", "#", "#"
            )
    print('\nPoint Attributes Spatially Joined with Polygon Attributes')
    
    tableExport = arcpy.conversion.TableToExcel(
            "OR_PS_Within_LS.shp", out_path + "OR_PS_Within_LS.xls")
    print('\n>>> Table of Point Data (with attached Polygon attributes) Exported to Excel')
    
    
except arcpy.ExecuteError:
    # If any error occurred when running the tool, print the messages
    print(arcpy.GetMessages())
    
except Exception as ex:
    print(ex.args[0])
