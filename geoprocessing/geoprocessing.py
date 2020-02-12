import arcpy
import pandas as pd


arcpy.env.overwriteOutput = True


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
