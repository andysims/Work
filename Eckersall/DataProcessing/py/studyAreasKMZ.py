import os, csv, arcpy
# import psycopg2, shutil

# KMZ Export Location
kmzDir = "C:/DIR/PATH"

if os.path.exists(kmzDir) == False:
	os.mkdir(kmzDir)
	print("KMZ directory has been created:\t\n" + kmzDir)
else:
    print("KMZ directory exists:\t\n" + kmzDir)


# Set workspace
arcpy.overwriteoutput = True
workspace = kmzDir + "/Study Areas/study_areas.mxd"
arcpy.env.workspace = workspace

company_lookup_csv = kmzDir + "/Study Areas/company_lookup.csv"

with open(company_lookup_csv) as f:
	reader = csv.reader(f, delimiter='|')
	company_lookup = list(reader)

for company in company_lookup:
		sac = company[0]
		co_name = company[1]
		co_name = co_name.replace('&', 'AND')
		co_name = co_name.replace('.', '')
		co_name = co_name.replace(',', '')
		co_name = co_name.replace('(', '- ')
		co_name = co_name.replace('/', '')
		co_name = co_name.replace(')', '')
		co_name = co_name.replace('\\', '')
		filename = sac +"_"+ co_name
        # mainDirPath = kmzDir + "/" + st_full
        # dirName = mainDirPath + "/" + st_county
		print("Processing " + filename)

        #if os.path.isdir(mainDirPath):
                #if os.path.isdir(dirName):
                #        os.rmdir(dirName)
                #        os.mkdir(dirName)
                #else:
                #        os.mkdir(dirName)
		# change definition query
		mxd = arcpy.mapping.MapDocument(workspace)
		df = arcpy.mapping.ListDataFrames(mxd)[0]
		co_extent = arcpy.mapping.ListLayers(mxd)[0]
		co_extent.definitionQuery = "sac = '{}'".format(sac)
        # update map view
		Extent = co_extent.getExtent(True)
		df.extent = Extent
		arcpy.RefreshActiveView()
		mxd.saveACopy(kmzDir + "/Study Areas/study_areas_current.mxd", "10.3")
		#arcpy.MapToKML_conversion(mxd, "Layers", filename, "0", "NO_COMPOSITE", "VECTOR_TO_IMAGE", "DEFAULT", "1024", "96", "CLAMPED_TO_GROUND")
		arcpy.MapToKML_conversion(in_map_document=kmzDir+"/Study Areas/study_areas_current.mxd", data_frame="Layers", out_kmz_file="C:/KMZ/DIR/Study Areas/Companies/" + filename + ".kmz", map_output_scale="0", is_composite="NO_COMPOSITE", is_vector_to_raster="VECTOR_TO_IMAGE", extent_to_export="DEFAULT", image_size="1024", dpi_of_client="96", ignore_zvalue="CLAMPED_TO_GROUND")
		os.remove(kmzDir+"/Study Areas/study_areas_current.mxd")
