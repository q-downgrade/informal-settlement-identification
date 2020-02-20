from data import data
from geoprocessing import *


wd = 'Z:/Dropbox/General_Assembly/Projects/project_5/data'
arcpy.env.overwriteOutput = True
arcpy.env.outputMFlag = "Disabled"


for g in data.keys():

    if (g == 'sp') | (g == 'rj'):
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

        # population data
        clip_raster(
            f"{wd}/{data['population']}",
            f"{wd}/processing/processing.gdb/{g}_target_study_area",
            f"{wd}/processing/processing.gdb/{g}_pop",
        )

        raster_to_integer(
            f"{wd}/processing/processing.gdb/{g}_pop",
            f"{wd}/processing/processing.gdb/{g}_pop_int",
        )

        raster_to_polygon(
            f"{wd}/processing/processing.gdb/{g}_pop_int",
            f"{wd}/processing/processing.gdb/{g}_pop_int_poly",
        )

        calculate_area(
            f"{wd}/processing/processing.gdb/{g}_pop_int_poly",
            "orig_pop_grid_area",
            "squaremeters",
        )

        intersect(
            f"{wd}/processing/processing.gdb/{g}_pop_int_poly",
            f"{wd}/processing/processing.gdb/{g}_geog_complete",
            f"{wd}/processing/processing.gdb/{g}_geog_int_pop_poly",
        )  # intersect geog and pop grid

        calculate_area(
            f"{wd}/processing/processing.gdb/{g}_geog_int_pop_poly",
            f"new_int_area",
            "squaremeters",
        )

        add_field_calculate(
            f"{wd}/processing/processing.gdb/{g}_geog_int_pop_poly",
            'pct_orig_area',
            'FLOAT',
            "!new_int_area! / !orig_pop_grid_area!",
        )

        add_field_calculate(
            f"{wd}/processing/processing.gdb/{g}_geog_int_pop_poly",
            'population_estimate',
            'FLOAT',
            "!pct_orig_area! * !gridcode!",
        )

        pop = feature_class_to_dataframe(
            f"{wd}/processing/processing.gdb/{g}_geog_int_pop_poly",
        )

        pop_g = pop[[
            "CD_GEOCODI",
            'population_estimate',
        ]].groupby(
            ["CD_GEOCODI"],
            as_index=False,
        ).sum()

        pop_g.columns = [x.lower() for x in pop_g.columns]
        # end population data

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
        print(len(master_df.index), 'line 98')
        master_df.columns = [x.lower() for x in master_df.columns]

        for i in ['sao_paulo', 'brazil']:  # 'airbnb',
            print(i)
            df = feature_class_to_dataframe(
                f"{wd}/input/real_estate/{i}/{i}.shp"
            )

            for c in list(df['property_t'].unique()):
                c = c.lower()
                print(f'    {c}')
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
                    print(len(master_df.index), 'line 134')
                    master_df = master_df.merge(
                        re_g,
                        left_on=census_tract_uid.lower(),
                        right_on=f'{i}_{c.lower()}_{census_tract_uid.lower()}',
                        how='left',
                    )
                    print(len(master_df.index), 'line 141')
                    master_df.drop(columns=[
                        f'{i}_{c.lower()}_{census_tract_uid.lower()}',
                        f'{i}_{c.lower()}_price',
                    ], inplace=True)

                # distance to nearest real estate locations
                p_gdb = 'processing/processing.gdb'
                near_table(
                    f"{wd}/{p_gdb}/{g}_geog_complete",
                    f"{wd}/input/real_estate/{i}/{i}_{c}.shp",
                    f"{wd}/{p_gdb}/{g}_geog_{i}_{c.lower()}_near",
                )

                nl = feature_class_to_dataframe(
                    f"{wd}/{p_gdb}/{g}_geog_{i}_{c.lower()}_near",
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
                    how='left'
                )

                nl[f'{i}_{c.lower()}_near_price'] = nl['price']

                nl.drop(
                    columns=[
                        f'{i}_{c.lower()}_objectid',
                        'FID',
                        'price',
                    ],
                    inplace=True,
                )

                print(len(master_df.index), 'line 185')

                if len(nl.index) > 0:
                    # nl = nl.merge(
                    #     pt,
                    #     how='left',
                    #     right_on='FID',
                    #     left_on=f'{i}_{c.lower()}_near_fid',
                    # )
                    print('nl', nl.shape, nl.columns)
                    print(len(master_df.index), 'line 196')

                    master_df = master_df.merge(
                        nl,
                        how='left',
                        left_on='objectid',
                        right_on=f'{i}_{c.lower()}_in_fid',
                    )

                    print(len(master_df.index), 'line 205')

                if g == 'sp':
                    # kernel density of listing locations
                    # kernel density of listing locations
                    # kernel density of listing locations
                    project_data(
                        f"{wd}/processing/processing.gdb/{g}_geog_int_{i}_{c}",
                        f"{wd}/processing/processing.gdb/{g}_geog_int_{i}_{c}_proj",
                        data["projections"]["WGS_1984_UTM_Zone_23S_EPSG"],
                    )

                    ex = 'proj_kd_c0500_r5000'
                    kernel_density(
                        f"{wd}/processing/processing.gdb/{g}_geog_int_{i}_{c}_proj",
                        f"{wd}/processing/processing.gdb/{g}_geog_int_{i}_{c}_{ex}",
                        500,
                        5000,
                        population_field="NONE",
                        area_units="SQUARE_KILOMETERS",
                    )

                    ep = ex + '_point'
                    raster_to_point(
                        f"{wd}/processing/processing.gdb/{g}_geog_int_{i}_{c}_{ex}",
                        f"{wd}/processing/processing.gdb/{g}_geog_int_{i}_{c}_{ep}",
                    )

                    ec = ep + '_int_census_tracts'
                    intersect(
                        f"{wd}/processing/processing.gdb/{g}_geog_complete",
                        f"{wd}/processing/processing.gdb/{g}_geog_int_{i}_{c}_{ep}",
                        f"{wd}/processing/processing.gdb/{g}_geog_int_{i}_{c}_{ec}",
                    )

                    kd = feature_class_to_dataframe(
                        f"{wd}/processing/processing.gdb/{g}_geog_int_{i}_{c}_{ec}",
                    )[["CD_GEOCODI", 'grid_code']]

                    kd.columns = [x.lower() for x in kd.columns]

                    kd[f'{g}_{i}_{c}_kernel_density'] = kd['grid_code'].round(6)

                    kd_g = kd[
                        ["cd_geocodi", f'{g}_{i}_{c}_kernel_density']].groupby(
                        "cd_geocodi",
                        as_index=False,
                    ).mean()

                    master_df = master_df.merge(
                        kd_g,
                        how='left',
                        left_on="cd_geocodi",
                        right_on="cd_geocodi",
                    )
                    # kernel density of listing locations
                    # kernel density of listing locations
                    # kernel density of listing locations

        # listings.columns = [x.lower() for x in listings.columns]  # force lcas
        master_df.columns = [x.lower() for x in master_df.columns]

        print(len(master_df.index), 'line 210')
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

        master_df.fillna(0, inplace=True)

        master_df = master_df[master_df.columns.drop(
            list(master_df.filter(regex='in_fid'))
        )]

        print(pop_g.head())
        master_df = master_df.merge(
            pop_g,
            how='left',
            on=census_tract_uid.lower(),
        )

        master_df.to_csv(
            f"{wd}/output/{g}_geoprocessing.csv",
            index=False,
        )
