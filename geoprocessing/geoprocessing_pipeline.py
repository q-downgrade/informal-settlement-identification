from data import data
from geoprocessing import *


wd = 'Z:/Dropbox/General_Assembly/Projects/project_5/data'
arcpy.env.overwriteOutput = True
arcpy.env.outputMFlag = "Disabled"


for g in data.keys():

    if (g == "real_estate") | (g == "projections"):  # sp or rj
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

        study_area_circle(
            f"{wd}/processing/processing.gdb/{g}_target",
            f"{wd}/processing/processing.gdb/{g}_target_study_area",
        )

        select_overlapping_data(
            f"{wd}/processing/processing.gdb/{g}_target_study_area",
            f"{wd}/processing/processing.gdb/{g}_geog",
            f"{wd}/processing/processing.gdb",
            f"{g}_geog_complete",
            message=True,
        )

        geog_complete = feature_class_to_dataframe(
            f"{wd}/processing/processing.gdb/{g}_geog_complete"
        )

        intersect(
            f"{wd}/processing/processing.gdb/{g}_geog_complete",
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

        master_df.columns = [x.lower() for x in master_df.columns]

        for i in ['airbnb', 'sao_paulo', 'brazil']:
            print(i)
            df = feature_class_to_dataframe(
                f"{wd}/input/real_estate/{i}/{i}.shp"
            )

            for c in list(df['property_t'].unique()):
                c = c.lower()
                print(c)
                intersect(
                    f"{wd}/processing/processing.gdb/{g}_geog_complete",
                    f"{wd}/input/real_estate/{i}/{i}_{c}.shp",
                    f"{wd}/processing/processing.gdb/{g}_geog_int_{i}_{c}",
                )  # create count of real estate listings per census tract

                re = feature_class_to_dataframe(
                    f"{wd}/processing/processing.gdb/{g}_geog_int_{i}_{c}",
                )

                if len(re.index) > 0:
                    re.columns = [f'{i}_{c}_{x.lower()}' for x in re.columns]

                    re_g = re[[
                        f'{i}_{c.lower()}_{census_tract_uid.lower()}',
                        f'{i}_{c.lower()}_price',
                    ]].groupby(
                        [f'{i}_{c.lower()}_{census_tract_uid.lower()}'],
                        as_index=False,
                    ).count()

                    re_g[f'{i}_{c.lower()}_count_listings'] = re_g[
                        f'{i}_{c.lower()}_price'
                    ]

                    master_df = master_df.merge(
                        re_g,
                        left_on=census_tract_uid.lower(),
                        right_on=f'{i}_{c.lower()}_{census_tract_uid.lower()}',
                        how='left',
                    )

                    master_df.drop(columns=[
                        f'{i}_{c.lower()}_{census_tract_uid.lower()}',
                        f'{i}_{c.lower()}_price',
                    ], inplace=True)

                # distance to nearest real estate locations
                near_table(
                    f"{wd}/processing/processing.gdb/{g}_geog_complete",
                    f"{wd}/input/real_estate/{i}/{i}_{c}.shp",
                    f"{wd}/processing/processing.gdb/{g}_geog_{i}_{c.lower()}_near",
                )

                nl = feature_class_to_dataframe(
                    f"{wd}/processing/processing.gdb/{g}_geog_{i}_{c.lower()}_near",
                )

                pt = feature_class_to_dataframe(
                    f"{wd}/input/real_estate/{i}/{i}_{c}.shp"
                )

                nl.columns = [
                    f'{i}_{c.lower()}_{x.lower()}' for x in nl.columns
                ]

                nl = nl.merge(
                    pt[['FID', 'price']],
                    left_on=f'{i}_{c.lower()}_near_fid',
                    right_on='FID',
                )

                nl = nl.drop(
                    columns=[
                        f'{i}_{c.lower()}_objectid',
                        f'{i}_{c.lower()}_in_fid',
                        'FID',
                    ],
                    inplace=True,
                )

                if len(nl.index) > 0:
                    master_df = master_df.merge(
                        nl,
                        how='left',
                        left_on='objectid',
                        right_on=f'{i}_{c.lower()}_in_fid',
                    )

        # listings.columns = [x.lower() for x in listings.columns]  # force lcas
        master_df.columns = [x.lower() for x in master_df.columns]

        # listings_g.to_csv(
        #     f"{wd}/output/{g}_test_listings.csv",
        #     index=False,
        # )

        # master_df = master_df.merge(
        #     listings_g[[
        #         census_tract_uid.lower(),
        #         'real_estate_count_listings',
        #     ]],
        #     how='left',
        #     on=census_tract_uid.lower(),
        # )

        # master_df[[
        #     census_tract_uid.lower(),
        #     'geog_orig_area',
        #     'favela_present',
        #     'favela_area_squaremeters',
        #     'real_estate_count_listings',
        #     'real_estate_objectid',
        #     'real_estate_in_fid',
        #     'real_estate_near_fid',
        #     'real_estate_near_dist',
        #     'real_estate_near_angle'
        # ]]

        master_df.drop(
            columns=[
                'objectid',
                'shape',
                'id',
                'tipo',
                'cd_geocodb',
                'nm_bairro',
                'cd_geocods',
                'cd_geocodd',
                'cd_geocodm',
                'shape_length',
                'shape_area',
            ],
            inplace=True,
        )

        master_df.to_csv(
            f"{wd}/output/{g}_master.csv",
            index=False,
        )

        # categories from kaggle set
        #       ph - private home
        #       apartment
        #       store
        #       house

        # create population estimate for census tract (aka geog)
        # post dataset to s3
