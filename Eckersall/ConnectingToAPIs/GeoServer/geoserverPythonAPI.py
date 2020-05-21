import requests
from geoserver.catalog import Catalog

# Set cat variable
cat = Catalog('http://url/geoserver/rest/', username="user", password="password")

# Create Workspace
#ws = cat.create_workspace('ws_name','http://uri/ws_name')
ws = cat.get_workspace('ws_name')

# Create Store from PostGIS
ds = cat.create_datastore('db_name','ws_name')

ds.connection_parameters.update(host='host', port='5432', database='db_name', user='user', passwd='password', dbtype='postgis', schema='public')

cat.save(ds)

# Add Layers from Postgres
ft = cat.publish_featuretype('table_name', ds, 'EPSG:3857', srs='EPSG:3857')

cat.save(ft)
