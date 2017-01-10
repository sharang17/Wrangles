"""
Map 911 rows to neighborhoods

https://data.baltimorecity.gov/Geographic/Study-Area/gi4i-vbvc
http://stackoverflow.com/questions/7861196/check-if-a-geopoint-with-latitude-and-longitude-is-within-a-shapefile

"""

import fiona
import shapely.geometry
import pandas as pd
import ipdb
import json

service_data = pd.read_csv(
    "/root/Development/CSE519/BaltimoreRanking-519/Data/911.csv")

neighborhoods = {}
rows_with_errors = []
with fiona.open("/root/Development/CSE519/BaltimoreRanking-519/Data/baltimore_neighborhoods/geo_export_08ed7f27-96f0-4be4-946a-c7cb3e3cfc81.shp") as fiona_collection:
    # try latitude and longitude against all shapes in shapefile
    shapefile_records = list(fiona_collection)
    shape_dict = {}
    for record in shapefile_records:
        shape_dict[record["properties"]["label"]] = shapely.geometry.asShape(record[
                                                                             'geometry'])

    # for row_num, series in service_data.iterrows():
    for sample in range(0, 5000):
        series = service_data.sample()
        lat_long_list = series['location'].values[0].split(",")
        try:
            lat = float(lat_long_list[0][1:])
            longit = float(lat_long_list[1][:-1])
        except:
            # rows_with_errors.append(row_num)
            rows_with_errors.append(series.index[0])
            continue

        # longitude, latitude
        point = shapely.geometry.Point(
            longit, lat)

        # Alternative: if point.within(shape)
        for neighborhood in shape_dict:
            if shape_dict[neighborhood].contains(point):
                # appears to be faster than shape.contains(point)
                # if point.within(shape):
                try:
                    # neighborhoods[record['properties']
                    #              ['label']].append(series.index[0])
                    neighborhoods[neighborhood].append(int(series.index[0]))
                except Exception as e:
                    # neighborhoods[record['properties']
                    #              ['label']] = [series.index[0]]
                    neighborhoods[neighborhood] = [int(series.index[0])]

with open("/root/Development/CSE519/BaltimoreRanking-519/Data/911_mapping.csv", "w") as fp:
    ipdb.set_trace()
    json.dump(neighborhoods, fp)
