import arcpy
import pandas as pd
import uuid
import json


arcpy.env.overwriteOutput = True
arcpy.env.outputMFlag = "Disabled"


def calculate_area(in_fc, area_field_name, area_units):
    arcpy.AddField_management(
        in_table=in_fc,
        field_name=area_field_name,
        field_type="DOUBLE"
    )

    arcpy.CalculateField_management(
        in_table=in_fc,
        field=area_field_name,
        expression="!shape.area@{}!".format(area_units),
        expression_type="PYTHON",
        code_block="",
    )  # refactor this to be subset of add_field_calculate


def fc_to_fc(input_fc, output_location, output_filename, expression=None):
    if expression:
        arcpy.FeatureClassToFeatureClass_conversion(
            input_fc,
            output_location,
            output_filename,
            expression,
        )
    else:
        arcpy.FeatureClassToFeatureClass_conversion(
            input_fc,
            output_location,
            output_filename,
        )


def feature_class_to_dataframe(in_fc):
    field_list = get_fc_fields(in_fc)
    df = pd.DataFrame([row for row in arcpy.da.SearchCursor(in_fc, field_list)])
    if len(df.index) > 0:
        df.columns = field_list
        return df
    else:
        print("            empty dataframe")
        return pd.DataFrame()
    # check out https://joelmccune.com/arcgis-to-pandas-data-frame-v2-0/


def get_fc_fields(fc):
    field_names = []
    fields = arcpy.ListFields(fc)
    for field in fields:
        field_names.append(field.name)
    return field_names


def intersect(in_fc_1, in_fc_2, output_fc, attributes="ALL"):
    arcpy.Intersect_analysis(
        "{} #;{} #".format(in_fc_1, in_fc_2),
        out_feature_class=output_fc,
        join_attributes=attributes,
        cluster_tolerance="-1 Unknown",
        output_type="INPUT",
    )


def dissolve_on_fields(input_fc, output_fc, dissolve_fields):
    arcpy.Dissolve_management(input_fc, output_fc, dissolve_fields)


def point_table_to_feature_class(
        input_table,
        input_x_column,
        input_y_column,
        spatial_reference_info,
        output_location,
        output_layer_name,
):
    uid = generate_uuid()

    arcpy.MakeXYEventLayer_management(
        table=input_table,
        in_x_field=input_x_column,
        in_y_field=input_y_column,
        out_layer="in_memory_layer_{}".format(uid),
        spatial_reference=spatial_reference_info,
        in_z_field="",
    )

    arcpy.FeatureClassToFeatureClass_conversion(
        in_features="in_memory_layer_{}".format(uid),
        out_path=output_location,
        out_name=output_layer_name,
    )


def generate_uuid():
    return uuid.uuid4().hex


def delete_fields(input_table, list_drop_fields):
    arcpy.DeleteField_management(
        in_table=input_table,
        drop_field=';'.join(list_drop_fields),
    )


def near_table(in_features, near_features, out_table):
    arcpy.GenerateNearTable_analysis(
        in_features,
        near_features,
        out_table,
        angle='ANGLE',
        method='GEODESIC',
        search_radius='10000 kilometers'
    )


def split_by_attributes(input_fc, workspace, split_fields):
    arcpy.SplitByAttributes_analysis(
        Input_Table=input_fc,
        Target_Workspace=workspace,
        Split_Fields=split_fields,
    )


def add_field_calculate(
        in_fc,
        new_field_name,
        new_field_type,
        expression,
):
    arcpy.AddField_management(
        in_table=in_fc,
        field_name=new_field_name,
        field_type=new_field_type,
    )

    arcpy.CalculateField_management(
        in_table=in_fc,
        field=new_field_name,
        expression=expression,
        expression_type="PYTHON",
        code_block="",
    )


def select_features_by_query(
        input_table,
        output_table,
        query,
):
    arcpy.Select_analysis(
        in_features=input_table,
        out_feature_class=output_table,
        where_clause=query,
    )


def select_overlapping_data(
        select_feature,
        select_from_dataset,
        output_location,
        output_layer_name,
        message=True,
):
    uid = generate_uuid()

    arcpy.MakeFeatureLayer_management(
        select_from_dataset,
        'select_from_dataset_{}'.format(uid),
    )

    arcpy.SelectLayerByLocation_management(
        'select_from_dataset_{}'.format(uid),
        "INTERSECT",
        select_feature,
        search_distance="",
        selection_type="NEW_SELECTION",
        invert_spatial_relationship="NOT_INVERT",
    )

    arcpy.FeatureClassToFeatureClass_conversion(
        'select_from_dataset_{}'.format(uid),
        output_location,
        output_layer_name
    )

    arcpy.Delete_management('select_from_dataset_{}'.format(uid))

    if message:
        print('    selection complete for {}'.format(select_from_dataset))


def study_area_circle(in_fc, out_fc):
    arcpy.MinimumBoundingGeometry_management(
        in_features=in_fc,
        out_feature_class=out_fc,
        geometry_type="CIRCLE",
        group_option="ALL",
        group_field="",
        mbg_fields_option="NO_MBG_FIELDS",
    )


def read_json(json_file):
    with open(json_file) as f:
        return json.load(f)


def clip_raster(
        input_raster,
        input_clip_geography,
        output_raster,
):
    arcpy.Clip_management(
        in_raster=input_raster,
        out_raster=output_raster,
        in_template_dataset=input_clip_geography,
        clipping_geometry="NONE",
        maintain_clipping_extent="NO_MAINTAIN_EXTENT",
    )


def raster_to_integer(input_raster, output_raster):
    arcpy.gp.RasterCalculator_sa(
        f'Int("{input_raster}")',
        output_raster,
    )


def raster_to_polygon(input_raster, output_polygon_fc):
    arcpy.RasterToPolygon_conversion(
        in_raster=input_raster,
        out_polygon_features=output_polygon_fc,
        simplify="NO_SIMPLIFY",
        raster_field="Value",
        create_multipart_features="SINGLE_OUTER_PART",
        max_vertices_per_feature="",
    )


def raster_to_point(input_raster, output_point_fc):
    arcpy.RasterToPoint_conversion(
        in_raster=input_raster,
        out_point_features=output_point_fc,
        raster_field="Value",
    )


def project_data(
        input_fc,
        output_fc,
        out_coordinate_system,
):
    arcpy.Project_management(
        in_dataset=input_fc,
        out_dataset=output_fc,
        out_coor_system=out_coordinate_system,
    )


def kernel_density(
        input_fc,
        output_raster,
        cell_size,
        search_radius,
        population_field="NONE",
        area_units="SQUARE_KILOMETERS",
):
    arcpy.gp.KernelDensity_sa(
        input_fc,
        population_field,
        output_raster,
        cell_size,
        search_radius,
        area_units,
    )
