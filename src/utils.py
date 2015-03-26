from os.path import isfile


def read(path):
    """Reads data in cron file"""
    raw_f = open_path(path)
    data = raw_f.readlines()
    raw_f.close()
    return data


def write(path, data):
    """Writes data in cron file"""
    raw_f = open(path, 'w+')
    raw_f.write(data + '\n')
    raw_f.close()