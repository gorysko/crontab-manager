from os import getlogin
from os import exists
from os import mkdir
from os.path import abspath
from os.path import join


def get_path(path=None):
	if path is None:
		path = join(abspath(__file__), '../data/')
	return join(path, getlogin())


def check_dir(path):
	if exists(path) is None:
		mkdir(path)


def put_data(path, data):
	pass


def get_data(path):
	pass
	