#!/usr/bin/python

#
# SCRIPT
#   msat_ls_cf_cc.py
# DESCRIPTION
# DEPENDENCIES
#   You need a Satellite server running to which this client
#   can connect.
# FAILURE
# AUTHORS
#   Date strings made with 'date +"\%Y-\%m-\%d \%H:\%M"'.
#   Allard Berends (AB), 2013-02-24 13:07
# HISTORY
# LICENSE
#   Copyright (C) 2013 Allard Berends
# 
#   msat_ls_cf_cc.py is free software; you can
#   redistribute it and/or modify it under the terms of the
#   GNU General Public License as published by the Free
#   Software Foundation; either version 3 of the License, or
#   (at your option) any later version.
#
#   msat_ls_cf_cc.py is distributed in the hope that it
#   will be useful, but WITHOUT ANY WARRANTY; without even
#   the implied warranty of MERCHANTABILITY or FITNESS FOR A
#   PARTICULAR PURPOSE. See the GNU General Public License
#   for more details.
#
#   You should have received a copy of the GNU General
#   Public License along with this program; if not, write to
#   the Free Software Foundation, Inc., 59 Temple Place -
#   Suite 330, Boston, MA 02111-1307, USA.
# DESIGN
#

import config
import optparse
import sys
import xmlrpclib

usage = '''list the config channels containing the specified config file'''

description = '''This script lists the config channels that contain the specified config file.'''

parser = optparse.OptionParser(
  usage = usage,
  version = '1.6',
  description = description,
)
parser.add_option(
  "-x",
  "--xml-help",
  action = "callback",
  callback = config.print_xmlhelp,
  help = "Print help in XML format",
)

parser.add_option(
  "-f",
  "--params-file",
  action = "callback",
  callback = config.parse_path,
  dest = "params_file",
  type = "string",
  default = '.sat.conf',
  help = "path to the parameter file",
)

parser.add_option(
  "-u",
  "--satellite-url",
  action = "callback",
  callback = config.parse_url,
  dest = "satellite_url",
  type = "string",
  default = None,
  help = "Satellite RPC API URL to use",
)
parser.add_option(
  "-a",
  "--satellite-login",
  action = "callback",
  callback = config.parse_string,
  dest = "satellite_login",
  type = "string",
  default = None,
  help = "admin account to log in with on Satellite",
)
parser.add_option(
  "-p",
  "--satellite-password",
  action = "callback",
  callback = config.parse_string,
  dest = "satellite_password",
  type = "string",
  default = None,
  help = "password belonging to Satellite admin account",
)

parser.add_option(
  "-n",
  "--configpath-path",
  action = "callback", 
  callback = config.parse_string,
  dest = "configpath_path",
  type = "string",
  default = None,
  help = "path of file or dir"
)
(options, args) = config.get_conf(parser)

if options.configpath_path is None:
  parser.error('Error: specify path, -n or --configpath-path')

# Get session key via auth namespace.
client = xmlrpclib.ServerProxy(options.satellite_url, verbose=0)
key = client.auth.login(options.satellite_login, options.satellite_password)

try:
  config_channels = client.configchannel.listGlobals(
    key,
  )
except xmlrpclib.Fault, e:
  print >> sys.stderr, str(e)

for i in config_channels:
	try:
		config_files = client.configchannel.listFiles(
			key,
			i['label']
		)
	except xmlrpclib.Fault, e:
		print >> sys.stderr, str(e)
		print >> sys.stderr, options.configchannel_label
		sys.exit(1)

	for f in config_files:
		if f.get('path') == options.configpath_path:
		  print i['label']

client.auth.logout(key)
