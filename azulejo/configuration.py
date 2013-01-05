# This file is part of azulejo
#
# Author: Pedro
#
# This code takes care of setting up or loading configurations.
# Do not edit this file directly. This is only used for bootstrap, once executed,
# this script will write configurations to ~/.azulejorc.js. If you want to
# personalize shortcuts and geometries, edit that file instead.
#

import json
import os.path
from collections import deque

conf_filename = "~/.azulejo/config.js"
filenames = { conf_filename : "initial_config.json", \
			 "~/.azulejo/Shortcuts/numpad.js" : "initial_shortcuts_numpad.json", \
			 "~/.azulejo/Shortcuts/no_numpad.js" : "initial_shortcuts_no_numpad.json"}
expanded_filenames = {}
shortcut_filenames = deque()

def read_file(path):
	"""Returns file content as string."""
	file_handler = open(path, 'r')
	content = file_handler.read()
	file_handler.close()
	return content

def get_initial_content(filename):
	"""Returns the initial values as string."""
	this_dir = os.path.dirname(os.path.abspath(__file__))
	#get the name of the appropriate initial file, then get the path of that file
	initial_config_path = os.path.join(this_dir, filenames[filename])
	return read_file(initial_config_path)

def create_initial_file(filename):
	#check if the path to the directory exists
	conf_dir = os.path.dirname(expanded_filenames[filename])
	if not os.path.exists(conf_dir):
		os.makedirs(conf_dir)
			
	"""Create a file with config values."""
	fw = open(expanded_filenames[filename], 'w')
	raw_json = get_initial_content(filename)
	fw.write(raw_json)
	fw.close()
	
def check_initial_files():

	for filename in filenames.iterkeys():
		
		expanded_filename = os.path.expanduser(filename)
		expanded_filenames[filename] = expanded_filename
		if not os.path.isfile(expanded_filename):
			print "Starting azulejo by creating file: '%s'" % (expanded_filename)
			create_initial_file(filename)

def get_config_data():
	
	expanded_conf_filename = expanded_filenames[conf_filename]
	json_string = read_file(os.path.expanduser(expanded_conf_filename))
	
	interpreted_json = json.loads(json_string)
	shortcut_data = interpreted_json[0]
	conf_data = interpreted_json[1:]
	
	shortcut_filename = os.path.expanduser(shortcut_data["shortcut_file_to_load"])
	json_string = read_file(shortcut_filename)
	conf_data += json.loads(json_string)
	
	return conf_data

def get_config_data_first_time():
	global shortcut_filenames
	check_initial_files()
	shortcut_filenames = deque(os.listdir(os.path.expanduser("~/.azulejo/Shortcuts")))
	for i in range(len(shortcut_filenames)):
		shortcut_filenames[i] = "~/.azulejo/Shortcuts/" + shortcut_filenames[i]
	return get_config_data()	   

def switch_shortcut_file():
	global shortcut_filenames
	expanded_conf_filename = expanded_filenames[conf_filename]
	json_string = read_file(os.path.expanduser(expanded_conf_filename))
	
	interpreted_json = json.loads(json_string)
	shortcut_data = interpreted_json[0]
	
	for filename in shortcut_filenames:
		if filename != shortcut_data["shortcut_file_to_load"]:
			shortcut_data["shortcut_file_to_load"] = filename
			break
		
	shortcut_filenames.rotate()
			
	print "Switched to Shortcut file: '%s'" % (shortcut_data["shortcut_file_to_load"])		
	conf_file = open(expanded_conf_filename, "w")
	conf_file.writelines(json.dumps([shortcut_data], sort_keys=True, indent=4))
	conf_file.close()
	
	return shortcut_data["shortcut_file_to_load"]
