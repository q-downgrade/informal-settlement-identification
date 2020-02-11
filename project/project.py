from tools.helpers import get_current_time, create_directory


def project():
    ml_time = get_current_time().replace('.', '_')
    g = 'geography'
    for wd in [
        f"data/{ml_time}_{g}/input",
        f'data/{ml_time}_{g}/processing',
        f'data/{ml_time}_{g}/output',
        f'data/{ml_time}_{g}/img',
    ]:
        create_directory(wd)

    return {'ml_time': ml_time, 'geography': g}
