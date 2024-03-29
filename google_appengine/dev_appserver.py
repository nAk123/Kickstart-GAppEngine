#!/usr/bin/env python
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#



"""Convenience wrapper for starting an appengine tool."""


import os
import re
import sys


if not hasattr(sys, 'version_info'):
  sys.stderr.write('Very old versions of Python are not supported. Please '
                   'use version 2.5 or greater.\n')
  sys.exit(1)
version_tuple = tuple(sys.version_info[:2])
if version_tuple < (2, 5):
  sys.stderr.write('Error: Python %d.%d is not supported. Please use '
                   'version 2.5 or greater.\n' % version_tuple)
  sys.exit(1)

DIR_PATH = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
SCRIPT_DIR = os.path.join(DIR_PATH, 'google', 'appengine', 'tools')
GOOGLE_SQL_DIR = os.path.join(
    DIR_PATH, 'google', 'storage', 'speckle', 'python', 'tool')



EXTRA_PATHS = [
  DIR_PATH,
  os.path.join(DIR_PATH, 'lib', 'antlr3'),
  os.path.join(DIR_PATH, 'lib', 'django_0_96'),
  os.path.join(DIR_PATH, 'lib', 'fancy_urllib'),
  os.path.join(DIR_PATH, 'lib', 'ipaddr'),
  os.path.join(DIR_PATH, 'lib', 'jinja2'),
  os.path.join(DIR_PATH, 'lib', 'protorpc'),
  os.path.join(DIR_PATH, 'lib', 'markupsafe'),
  os.path.join(DIR_PATH, 'lib', 'webob_0_9'),
  os.path.join(DIR_PATH, 'lib', 'webapp2'),
  os.path.join(DIR_PATH, 'lib', 'yaml', 'lib'),
  os.path.join(DIR_PATH, 'lib', 'simplejson'),
  os.path.join(DIR_PATH, 'lib', 'google.appengine._internal.graphy'),
]

API_SERVER_EXTRA_PATHS = [
  os.path.join(DIR_PATH, 'lib', 'argparse'),
]
API_SERVER_EXTRA_PATH_SCRIPTS = 'api_server'


OAUTH_CLIENT_EXTRA_PATHS = [
  os.path.join(DIR_PATH, 'lib', 'google-api-python-client'),
  os.path.join(DIR_PATH, 'lib', 'httplib2'),
  os.path.join(DIR_PATH, 'lib', 'python-gflags'),
]

OAUTH_CLIENT_EXTRA_PATH_SCRIPTS = '(appcfg|bulkloader)'


GOOGLE_SQL_EXTRA_PATHS = OAUTH_CLIENT_EXTRA_PATHS + [
  os.path.join(DIR_PATH, 'lib', 'enum'),
  os.path.join(DIR_PATH, 'lib', 'grizzled'),
  os.path.join(DIR_PATH, 'lib', 'oauth2'),
  os.path.join(DIR_PATH, 'lib', 'prettytable'),
  os.path.join(DIR_PATH, 'lib', 'sqlcmd'),
]

GOOGLE_SQL_EXTRA_PATH_SCRIPTS = 'google_sql'



SCRIPT_EXCEPTIONS = {
  "dev_appserver.py" : "dev_appserver_main.py"
}

SCRIPT_DIR_EXCEPTIONS = {
  'google_sql.py': GOOGLE_SQL_DIR,
}


def fix_sys_path(extra_extra_paths=()):
  """Fix the sys.path to include our extra paths."""
  extra_paths = EXTRA_PATHS[:]
  extra_paths.extend(extra_extra_paths)
  sys.path = extra_paths + sys.path


def run_file(file_path, globals_, script_dir=SCRIPT_DIR):
  """Execute the file at the specified path with the passed-in globals."""
  script_name = os.path.basename(file_path)

  if re.match(OAUTH_CLIENT_EXTRA_PATH_SCRIPTS, script_name):
    extra_extra_paths = OAUTH_CLIENT_EXTRA_PATHS
  elif re.match(GOOGLE_SQL_EXTRA_PATH_SCRIPTS, script_name):
    extra_extra_paths = GOOGLE_SQL_EXTRA_PATHS
  elif re.match(API_SERVER_EXTRA_PATH_SCRIPTS, script_name):
    extra_extra_paths = API_SERVER_EXTRA_PATHS
  else:
    extra_extra_paths = []
  fix_sys_path(extra_extra_paths)

  script_name = SCRIPT_EXCEPTIONS.get(script_name, script_name)
  script_dir = SCRIPT_DIR_EXCEPTIONS.get(script_name, script_dir)
  script_path = os.path.join(script_dir, script_name)
  execfile(script_path, globals_)


if __name__ == '__main__':
  run_file(__file__, globals())
