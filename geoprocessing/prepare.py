from data import data
from geoprocessing import *


wd = 'Z:/Dropbox/General_Assembly/Projects/project_5/data'

# create geospatial files
# point_table_to_feature_class(
#         f"{wd}/{data['rj']['airbnb_csv']}",
#         "longitude",
#         "latitude",
#         data["rj"]["wgs_84_srid"],
#         f"{wd}/input/airbnb/brazil",
#         "listings.shp",
# )
#
# delete_fields(
#     f"{wd}/input/airbnb/brazil/listings.shp",
#     [
#         "name",
#         "host_id",
#         "host_name",
#         "neighbourh",
#         "neighbou_1",
#         "room_type",
#         "minimum_ni",
#         "number_of_",
#         "last_revie",
#         "reviews_pe",
#         "calculated",
#         "availabili",
#     ],
# )

# create geospatial files
point_table_to_feature_class(
        f"{wd}/{data['sp']['listings_csv']}",
        "longitude",
        "latitude",
        data["rj"]["wgs_84_srid"],
        f"{wd}/input/real_estate/sao_paulo",
        "listings.shp",
)
