from data import data
from geoprocessing import *


wd = 'Z:/Dropbox/General_Assembly/Projects/project_5/data'

# create geospatial files
# point_table_to_feature_class(
#     f'{wd}/{data["real_estate"]["airbnb_rio_csv"]}',
#     "longitude",
#     "latitude",
#     data["projections"]["wgs_84_srid"],
#     f"{wd}/input/real_estate/airbnb",
#     "airbnb.shp",
# )
#
# delete_fields(
#     f'{wd}/{data["real_estate"]["airbnb_rio"]}',
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
#         "id",
#     ],
# )

# add_field_calculate(
#     f"{wd}/{data['real_estate']['airbnb_rio']}",
#     'property_t',
#     'TEXT',
#     "'airbnb'",
# )

# f'{wd}/{data["real_estate"]["airbnb_rio"]}',

for i in ['sao_paulo', 'brazil']:
    csv_name = f'{i}_csv'
    # create geospatial files
    point_table_to_feature_class(
        f"{wd}/{data['real_estate'][csv_name]}",
        "lon",
        "lat",
        data["projections"]["wgs_84_srid"],
        f"{wd}/input/real_estate/{i}",
        f"{i}.shp",
    )

    df = feature_class_to_dataframe(f"{wd}/input/real_estate/{i}/{i}.shp")

    for c in list(df['property_t'].unique()):
        select_features_by_query(
            f"{wd}/input/real_estate/{i}/{i}.shp",
            f"{wd}/input/real_estate/{i}/{i}_{c.lower()}.shp",
            f""" "property_t" = '{c}' """,
        )


for i in ['airbnb']:
    df = feature_class_to_dataframe(f"{wd}/input/real_estate/{i}/{i}.shp")

    for c in list(df['property_t'].unique()):
        select_features_by_query(
            f"{wd}/input/real_estate/{i}/{i}.shp",
            f"{wd}/input/real_estate/{i}/{i}_{c.lower()}.shp",
            f""" "property_t" = '{c}' """,
        )


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
