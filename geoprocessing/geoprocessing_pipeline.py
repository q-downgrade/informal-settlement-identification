from data import data
from geoprocessing import *


wd = 'Z:/Dropbox/General_Assembly/Projects/project_5/data'
arcpy.env.overwriteOutput = True
arcpy.env.outputMFlag = "Disabled"


for g in data.keys():

    # define study area extent for Sao Paolo/ Rio

    if g == 'potato':  # sp or rj
        pass
    else:
        print(f"running for {g}")
        geog = f"{wd}/{data[g]['census_tract']}"
        target = f"{wd}/{data[g]['favela']}"

        for i in [[geog, 'geog'], [target, 'target']]:
            fc_to_fc(
                i[0],
                f"{wd}/processing/processing.gdb/",
                f"{g}_{i[1]}",
            )

            calculate_area(
                f"{wd}/processing/processing.gdb/{g}_{i[1]}",
                f"{i[1]}_orig_area",
                "squaremeters",
            )  # create orig area for census tract (aka geog) & favela (aka tar)

        geog_complete = feature_class_to_dataframe(
            f"{wd}/processing/processing.gdb/{g}_geog"
        )

        intersect(
            f"{wd}/processing/processing.gdb/{g}_geog",
            f"{wd}/processing/processing.gdb/{g}_target",
            f"{wd}/processing/processing.gdb/{g}_geog_int_target",
        )  # intersect geog and target

        calculate_area(
            f"{wd}/processing/processing.gdb/{g}_geog_int_target",
            f"new_int_area",
            "squaremeters",
        )

        df = feature_class_to_dataframe(
            f"{wd}/processing/processing.gdb/{g}_geog_int_target",
        )

        census_tract_uid = "CD_GEOCODI"

        dfg = df[[
            census_tract_uid,
            f"{i[1]}_orig_area",
            "new_int_area",
        ]].groupby(
            [census_tract_uid, f"{i[1]}_orig_area"],
            as_index=False,
        ).sum()  # create sum favela area for census tract (aka geog)

        dfg['favela_present'] = 1  # create favela binary flag for census tract
        dfg['favela_area_squaremeters'] = dfg['new_int_area']

        dfg[[
            census_tract_uid,
            f"{i[1]}_orig_area",
            'favela_present',
            'favela_area_squaremeters'
        ]].to_csv(
            f"{wd}/processing/{g}_geog_int_target_sum.csv",
            index=False,
        )

        master_df = geog_complete.merge(
            dfg[[
                census_tract_uid,
                'favela_present',
                'favela_area_squaremeters',
            ]],
            how='left',
            on=census_tract_uid,
        )

        intersect(
            f"{wd}/processing/processing.gdb/{g}_geog",
            f"{wd}/{data[g]['listings']}",
            f"{wd}/processing/processing.gdb/{g}_geog_int_listings",
        )  # intersect geog and target

        listings = feature_class_to_dataframe(
            f"{wd}/processing/processing.gdb/{g}_geog_int_listings",
        )

        listings.columns = [x.lower() for x in listings.columns]  # force lcase
        master_df.columns = [x.lower() for x in master_df.columns]

        listings_g = listings[[
            census_tract_uid.lower(),
            "price",
        ]].groupby(
            [census_tract_uid.lower()],
            as_index=False,
        ).count()  # create sum favela area for census tract (aka geog)

        listings_g['count_listings'] = listings_g['price']

        listings_g.to_csv(
            f"{wd}/output/{g}_test_listings.csv",
            index=False,
        )

        master_df = master_df.merge(
            listings_g[[
                census_tract_uid.lower(),
                'count_listings',
            ]],
            how='left',
            on=census_tract_uid.lower(),
        )

        master_df[[
            census_tract_uid.lower(),
            'geog_orig_area',
            'count_listings',
            'favela_present',
            'favela_area_squaremeters',
        ]].to_csv(
            f"{wd}/output/{g}_master.csv",
            index=False,
        )
        # create count of real estate listings per census tract (aka geog)

        # create population estimate for census tract (aka geog)
        # create from geog to_csv function to create analytical dataset
        # post dataset to s3
        # have preliminary analytical dataset for rio for Q by noon
        # have preliminary analytical dataset for sp for Matteo by 5
