import os


def get_input_path(filename):
    return os.path.join('.', filename)


def get_output_path(filename):
    return os.path.join('.', 'webroot', 'data', filename)
