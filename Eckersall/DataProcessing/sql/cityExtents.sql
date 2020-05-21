/*
City Extents

Last updated: April 23, 2018

Purpose: Calculate city extents, and populates additional fields

Script does the following:
- creates a copied table called cityextents from city table
- adds/updates fields
- exports a CSV file

This script assumes the following:
- city and tax (downloaded via census.gov) exist in a Postgres table

Additional info:
- city extents were calculated using SRID: 3857 (Web Mercator)
- top priorities are CityName, max/min, & zipcode fields
- run this line to check the bounding box:
select "CityName", st_extent(geom) from cityextents order by "CityName";
- run this line to ensure cities aren't duplicated in table:
select "CityName", count(*) from cityextents group by "CityName" having count(*) > 1 order by "CityName";
*/

-- drop exiting cityextents table
drop table if exists cityextents;

-- creates new table from city table
create table cityextents as select
  st_union(geom) as geom,
  (initcap(city_name)) as "CityName",
  (st_xmax(st_union(geom))) as "maxX",
  (st_ymax(st_union(geom))) as "maxY",
  (st_xmin(st_union(geom))) as "minX",
  (st_ymin(st_union(geom))) as "minY"
  from city where city_type = 'City' group by city_name;

-- adds additional columns
alter table cityextents
  -- CityExtents
  add column zipcode varchar[],  -- array
  add column "LogoPath" varchar(150);

-- update zipcode field
update cityextents set zipcode = array(select distinct zcta5ce10 from zip where st_intersects(zip.geom,cityextents.geom));

-- update other fields
update cityextents set
  "LogoPath" = trim(concat('~/images/city_logos/',replace(initcap(lower("CityName")), ' ', ''),'.png'));

-- export to csv
COPY (select * from cityextents) TO 'specify_path/filename.csv' DELIMITER ',' CSV HEADER;
