"""
Last updated: 6/18/2020

This script creates a right of way (row) table
using geom and fips codes in parcels table.

Before running script make sure all records in
countyfips within parcels table are filled in.
"""

import us
import psycopg2

# Connects to Postgres
con = psycopg2.connect(
    dbname='db_name',
    user='user_name',
    host='localhost',
    port='port',
    password='password')

cur = con.cursor()

# Add dictionary {st, abbr, fips} to list
states = []

for st in us.states.STATES:
    st_lookup = us.states.lookup(str(st))
    abbr = str(st.abbr)
    state = {
        'st_name': str(st),
        'st_abbr': abbr,
        'fips': []
    }
    states.append(state)

# Select distinct county fips codes
for st in states:
    st_abbr = st['st_abbr']
    run_cmd = f'SELECT DISTINCT fips FROM counties WHERE st = \'{st_abbr}\''
    cur.execute(run_cmd)
    fip_list = cur.fetchall()
    fip_codes = []
    for code in fip_list:
        fip_codes.append(code[0])
    st['fips'] = fip_codes

# Drop/Create table
print('Dropping row table...')
drop_table = 'DROP TABLE IF EXISTS row'
cur.execute(drop_table)
print('Done.')
print('Creating row table...')
create_table =\
            f'CREATE TABLE row (id bigserial PRIMARY KEY, geom geometry(Polygon, 3857)) '\
            f'WITH (OIDS=FALSE);'
cur.execute(create_table)
print("Done.\n")

# Select from parcels table to create row and insert
for st in states:
    for fip in st['fips']:
        print(f'Creating row for fips {fip}...')
        cmd = f'INSERT INTO row (geom) ' \
              f'SELECT (ST_Dump(ST_Union(ST_SnapToGrid(geom,0.001)))).geom as geom ' \
              f'FROM parcels WHERE countyfips = \'{fip}\';'
        cur.execute(cmd)
        print(f'Done.\n')

# Create index
cur.execute('DROP INDEX IF EXISTS sidx_row_geom;')
cur.execute('CREATE INDEX sidx_row_geom ON row USING GIST (geom);')
print('Index has been created.')

# Commit
con.commit()
print('row table is updated.')
