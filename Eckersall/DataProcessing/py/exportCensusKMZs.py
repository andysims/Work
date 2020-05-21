import os, csv, arcpy
# import psycopg2, shutil

# KMZ Export Location
kmzDir = "C:/Directory/Location"

if os.path.exists(kmzDir) == False:
        os.mkdir(kmzDir)
        print("KMZ directory has been created:\t\n" + kmzDir)
else:
        print("KMZ directory exists:\t\n" + kmzDir)


# Set workspace
arcpy.overwriteoutput = True
workspace = kmzDir + "/blocks.mxd"
arcpy.env.workspace = workspace


"""
# Export county_fips from client DB to CSV if necessary
conn = psycopg2.connect(host="localhost",port=5432,database="db_name",user="user_name",password="password")

cur = conn.cursor()

if os.path.exists(kmzDir + "fips_lookup.csv") == False:
    cur.execute("""copy county_fips to 'kmzDir location/fips_lookup.csv' delimiter ',' csv """)
"""

# Create FIPS lookup list
fips_lookup_csv = kmzDir + "/fips_lookup.csv"  # TODO: remove _arizona

with open(fips_lookup_csv) as f:
    reader = csv.reader(f)
    fips_lookup = list(reader)

# Read fips lookup to create directory and set def query
# 1 = fips, 2 = st, 4 = county no space (county_nospc), 5 = st_full

for state in fips_lookup:
        mainDirName = kmzDir + "/" + state[5]
        if os.path.exists(mainDirName):
                os.rmdir(mainDirName)
                os.mkdir(mainDirName)
        else:
                os.mkdir(mainDirName)

for fips_rec in fips_lookup:
        fips = fips_rec[1]
        st = fips_rec[2]
        county = fips_rec[4]
        st_full = fips_rec[5]

        st_county = st + "_" + county
        mainDirPath = kmzDir + "/" + st_full
        dirName = mainDirPath + "/" + st_county

        print("Processing " + st_county)

        if os.path.isdir(mainDirPath):
                #if os.path.isdir(dirName):
                #        os.rmdir(dirName)
                #        os.mkdir(dirName)
                #else:
                #        os.mkdir(dirName)
		# change definition query
		mxd = arcpy.mapping.MapDocument(workspace)
		df = arcpy.mapping.ListDataFrames(mxd)[0]
		cb_layer = arcpy.mapping.ListLayers(mxd)[2]
		cb_layer.definitionQuery = "fips = '{}'".format(fips)
		cbg_layer = arcpy.mapping.ListLayers(mxd)[1]
		cbg_layer.definitionQuery = "fips = '{}'".format(fips)
		ct_layer = arcpy.mapping.ListLayers(mxd)[0]
		ct_layer.definitionQuery = "fips = '{}'".format(fips)
        # update map view
		Extent = cbg_layer.getExtent(True)
		df.extent = Extent
		arcpy.RefreshActiveView()
		mxd.saveACopy(kmzDir + "/blocksCurrent.mxd", "10.3")
		filename = dirName + "/" + st_county + ".kmz"
		#arcpy.MapToKML_conversion(mxd, "Layers", filename, "0", "NO_COMPOSITE", "VECTOR_TO_IMAGE", "DEFAULT", "1024", "96", "CLAMPED_TO_GROUND")
		arcpy.MapToKML_conversion(in_map_document=kmzDir+"/blocksCurrent.mxd", data_frame="Layers", out_kmz_file= kmzDir + st_full + "/" + st + "_" + county + ".kmz", map_output_scale="0", is_composite="NO_COMPOSITE", is_vector_to_raster="VECTOR_TO_IMAGE", extent_to_export="DEFAULT", image_size="1024", dpi_of_client="96", ignore_zvalue="CLAMPED_TO_GROUND")
		os.remove(kmzDir+"/blocksCurrent.mxd")
