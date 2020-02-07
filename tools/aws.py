import boto3
from boto3.s3.transfer import TransferConfig
import psycopg2


def aws_connect(access_key_id, secret_access_key):
    return boto3.Session(access_key_id, secret_access_key)


def s3_session_connect(session):
    return session.resource('s3')


def print_s3_buckets(s3_session):
    for bucket in s3_session.buckets.all():
        print(bucket.name)


def file_to_s3(s3_session, bucket_name, file_to_upload, filename_on_s3):
    data = open(file_to_upload, 'rb')
    s3_session.Bucket(bucket_name).put_object(
        Key=filename_on_s3,
        Body=data,
        ACL='public-read',
    )


def upload_file_to_s3(config, bucket_name, local_file, filename_on_s3):
    access_key_id = config['aws']['access_key_id']
    secret_access_key = config['aws']['secret_access_key']

    file_to_s3(
        s3_session_connect(aws_connect(access_key_id, secret_access_key)),
        bucket_name,
        local_file,
        filename_on_s3,
    )
    link = 'https://autoceqr.s3.amazonaws.com/{}'.format(filename_on_s3)
    print('    aws url: {}'.format(link))

    return link


def s3_client_connect(access_key_id, secret_access_key):
    return boto3.client(
        's3',
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key,
    )


def large_file_to_s3(s3_client, bucket_name, file_to_upload, filename_on_s3):
    gb = 1024 ** 3
    transfer_config = TransferConfig(multipart_threshold=5 * gb)

    s3_client.upload_file(
        file_to_upload,
        bucket_name,
        filename_on_s3,
        Config=transfer_config,
    )


def upload_large_file_to_s3(config, bucket_name, local_file, filename_on_s3):
    access_key_id = config['aws']['access_key_id']
    secret_access_key = config['aws']['secret_access_key']

    large_file_to_s3(
        s3_client_connect(access_key_id, secret_access_key),
        bucket_name,
        local_file,
        filename_on_s3,
    )
    link = 'https://autoceqr.s3.amazonaws.com/{}'.format(filename_on_s3)
    print('    aws url: {}'.format(link))

    return link


def connect_postgres_db(database_name, database_user, database_user_password, db_host_url, db_port=5432):
    return psycopg2.connect(
        database=database_name,
        user=database_user,
        password=database_user_password,
        host=db_host_url,
        port=db_port
    )


def get_cursor(connection):
    return connection.cursor()


def execute_sql(cursor, sql_statement):
    cursor.execute(sql_statement)


def list_tables(cursor):
    tables = []
    cursor.execute(
        """SELECT table_name FROM information_schema.tables
           WHERE table_schema = 'public'"""
    )

    for table in cursor.fetchall():
        print(table)
        tables.append(table)

    return tables
# https://stackoverflow.com/questions/50070877/postgres-psycopg2-create-table
# https://stackoverflow.com/questions/10598002/how-do-i-get-tables-in-postgres-using-psycopg2
