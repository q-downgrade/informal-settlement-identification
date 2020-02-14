from aws import *
from data import data
from geoprocessing import *


wd = 'Z:/Dropbox/General_Assembly/Projects/project_5/data'
config = read_json('config.json')

for g in data.keys():
    local_file = f"{wd}/output/{g}_master.csv",

    large_file_to_s3(
        s3_client_connect(config['access_key_id'], config['secret_access_key']),
        'general-assembly-project-5',
        local_file,
        f'{g}_master.csv"',
    )

    link = f'https://general-assembly-project-5.s3.amazonaws.com/{g}_master.csv'
    print('    aws url: {}'.format(link))
