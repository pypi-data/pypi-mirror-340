
import os
import sys
import inspect

def get_abs_path(rel_path="", up=0, follow_links=False):

	getpath = os.path.realpath if follow_links else os.path.abspath

	current_file = getpath(__file__)
	stack = inspect.stack()
	for frame in stack:
		caller = getpath(frame.filename)
		if caller != current_file:
			break

	file_path = os.path.dirname(getpath(caller))
	file_path = os.path.join(file_path, rel_path)
	ret_path  = getpath(file_path)

	for i in range(up):
		ret_path = os.path.dirname(ret_path)

	return ret_path


def add_abs_path(abs_path):
	if abs_path not in sys.path:
		sys.path += [abs_path]


def add_rel_path(rel_path, follow_links=False):
	add_abs_path(get_abs_path(rel_path, follow_links))


def join_path(*args):
	return os.path.join(*args)


def to_os_path(path, os=None):
	if os == 'linux':
		sep = '/'
	elif os == 'windows':
		sep = '\\'
	else:
		sep = os.sep
	return path.replace('/', sep).replace('\\', sep)


def get_basename(path, up=0, noext=False):
	for i in range(up):
		path = os.path.dirname(path)
	path = os.path.basename(path)
	if noext:
		path = os.path.splitext(path)[0]
	return path
