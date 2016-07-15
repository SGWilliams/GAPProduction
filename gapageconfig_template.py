#This is the config file for gapage.  Store it somewhere other than with the gapage code and data.

#Directory with spatial and aspatial datasets needed for gappack
data_directory = "xxxxxx/BasicPackage/data"

#Directory where some temp files should be stored (scratch workspace)
temp_directory = "xxxxxxxx"

#Pickle file with dictionary of wildlife centric classification
wildclass = data_directory + "/WildlifeMUClassification.pkl"

# Username and password for the GAP databases
server = ""
uid = raw_input("Username: ")
password = raw_input("Password: ")

#Path to modeling data layers
GAP_data = "xxx/xxxx/xxx"

#Path to the snap raster
snap_raster = data_directory + "/snapgrid"

#The path to the CONUS HUCs shapefile
hucs = GAP_data + "/Hucs.shp"

#Path to directory containing regional boundary shapefiles
region_shapefiles = GAP_data + "/regions"

#Path to shapefile of all regions
regions_shapefile = data_directory + "modeling_regions.shp"

#Path to directory containing Land Cover rasters used in modeling.
land_cover = GAP_data + "/LandCover"

#Path to directory containing completed species model outputs GEOtiffs for analyses
output_location = "xxx/xxxx/xxx"

#Added 7/13/2016
#Gapemail passwords
emailAddress = ""
emailPwd = ""
emailAccountServer = ''
emailDefaultToAddress = ""

#Directory to store output from richness analyses
richness_directory = "xxx/xxxx/xxx"

#Directory with metadata templates
meta_templates_dir = data_directory + "/metadata_templates"