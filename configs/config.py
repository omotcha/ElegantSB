"""
platform: any
env: any
name: config.py
project configurations
"""

import os

# platform specific
platform_delimiter = "/"

# project structure
configs_dir = os.path.abspath(os.path.dirname(__file__))
project_dir = os.path.split(configs_dir)[0]
tmp_dir = os.path.join(project_dir, "tmp")
example_dir = os.path.join(project_dir, "example")

############################################
# experimental settings
############################################

# Max Limit of Time of Action/Switch Pipe, enlarge it in case a song is longer than 10000 seconds
MAX_PIPE_TIME = 10000

# Do precision on time stored in Action/Switch Pipe,
# If less than 0 or not an integer, no precision on time will be performed
TIME_PRECISION = -1
