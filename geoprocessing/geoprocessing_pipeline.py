from data import data
from geoprocessing import *


wd = 'Z:/Dropbox/General_Assembly/Projects/project_5/data'

for g in data.keys():
    if g == 'rj':
        pass
    else:
        geog = f"{wd}/{data[g]['census_tract']}"
        target = f"{wd}/{data[g]['favela']}"
        # define study area extent for Sao Paolo/ Rio

        fc_to_fc(geog, f"{wd}/processing/geog/", f"{g}_geog.shp")

        calculate_area(
            f"{wd}/processing/geog/{g}_geog.shp",
            "orig_area",
            "squaremeters",
        )  # create orig area for census tract (aka geog)

        # create orig area for favela  (aka target)
        # create pct favela area for census tract (aka geog)
        # create favela binary flag for census tract (aka geog)
        # create population estimate for census tract (aka geog)
        # create count of real estate listings per census tract (aka geog)
        # create from geog to_csv function to create analytical dataset
        # post dataset to s3
        # have preliminary analytical dataset for rio for Q by noon
        # have preliminary analytical dataset for sp for Matteo by 5
