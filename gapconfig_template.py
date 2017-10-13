#This is the config file for gapage.  Store it somewhere other than with the gapage code and data.

############################     STUFF YOU HAVE TO CHANGE   ########################################

#Directory with spatial and aspatial datasets needed for gappack
data_directory = "xxxxxx/GAPProduction/data"

#Directory where some temp files should be stored (scratch workspace)
temp_directory = "xxxxxxxx"

#Path to modeling data layers
GAP_data = "xxx/xxxx/xxx"

#Username and password for the GAP databases
server = ""
uid = raw_input("Username: ")
password = raw_input("Password: ")
trusted = raw_input("Trusted (Yes/No)?")

#Gapemail passwords
emailAddress = ""
emailPwd = ""
emailAccountServer = ""
emailDefaultToAddress = ""

#Sciencebase credentials
sbUserName = ""
sbWord = ''''''


####################    STUFF YOU DON'T HAVE TO CHANGE  ############################################

#Path to the CONUS extent raster with top, left pixels for counting.
CONUS_extent = GAP_data + "/conus_ext_cnt"

#The path to the CONUS HUCs shapefile
hucs = GAP_data + "/Hucs.shp"

#Path to directory containing Land Cover rasters used in modeling.
land_cover = GAP_data + "/LandCover"

#Path to directory containing regional boundary shapefiles
region_shapefiles = GAP_data + "/regions"

#Pickle file with dictionary of wildlife centric classification
wildclass = data_directory + "/WildlifeMUClassification.pkl"

#Path to the snap raster
snap_raster = data_directory + "/snapgrid"

#Path to table with extents of each huc in Albers
HUC_Extents = data_directory + "/HUC_Extents.txt"

#Path to shapefile of all regions
regions_shapefile = data_directory + "modeling_regions.shp"
