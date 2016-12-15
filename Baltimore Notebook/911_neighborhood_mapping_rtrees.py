"""
Note on Rtrees:
http://gis.stackexchange.com/questions/120955/understanding-the-use-of-spatial-indexes/144764#144764


"""

import json
import rtree
import fiona
import shapely.geometry
import pandas as pd
import sys
import ipdb

neighborhoods = {}
rows_with_errors = []

fiona_collection = fiona.open(
    "/root/Development/CSE519/BaltimoreRanking-519/Data/baltimore_neighborhoods/geo_export_08ed7f27-96f0-4be4-946a-c7cb3e3cfc81.shp")

service_data = pd.read_csv(
    "/root/Development/CSE519/BaltimoreRanking-519/Data/911.csv")


# try latitude and longitude against all shapes in shapefile
shapefile_records = list(fiona_collection)
shape_dict = {}
for record in shapefile_records:
    shape_dict[record["properties"]["label"]] = shapely.geometry.asShape(record[
                                                                         'geometry'])

# create an empty spatial index object
index = rtree.index.Index()
for fid, feature in fiona_collection.items():
    geometry = shapely.geometry.shape(feature["geometry"])
    index.insert(fid, geometry.bounds)

for row_num, series in service_data.iterrows():
    lat_long_list = series['location'].split(",")
    try:
        lat = float(lat_long_list[0][1:])
        longit = float(lat_long_list[1][:-1])
    except:
        # rows_with_errors.append(row_num)
        rows_with_errors.append(series.name)
        continue

    point = shapely.geometry.Point(longit, lat)
    fids = [int(i) for i in index.intersection(point.bounds)]
    for fid in fids:
        shape = shapely.geometry.shape(fiona_collection[fid]['geometry'])
        if shape.contains(point):
            try:
                neighborhoods[fiona_collection[fid][
                    "properties"]['label']].append(int(series.name))
                break
            except Exception as e:
                neighborhoods[fiona_collection[fid][
                    "properties"]['label']] = [int(series.name)]
                break

with open("/root/Development/CSE519/BaltimoreRanking-519/Data/911_mapping_rtree_2.csv", "w") as fp:
    json.dump(neighborhoods, fp)
