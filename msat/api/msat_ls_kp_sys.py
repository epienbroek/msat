#!/usr/bin/python

#
# SCRIPT
#   msat_ls_kp_sys.py
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
#   msat_ls_kp_sys.py is free software; you can
#   redistribute it and/or modify it under the terms of the
#   GNU General Public License as published by the Free
#   Software Foundation; either version 3 of the License, or
#   (at your option) any later version.
#
#   msat_ls_kp_sys.py is distributed in the hope
#   that it will be useful, but WITHOUT ANY WARRANTY;
#   without even the implied warranty of MERCHANTABILITY or
#   FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
#   Public License for more details.
#
#   You should have received a copy of the GNU General
#   Public License along with this program; if not, write to
#   the Free Software Foundation, Inc., 59 Temple Place -
#   Suite 330, Boston, MA 02111-1307, USA.
# DESIGN
#

import config
import optparse
import re
import sys
import time
import xmlrpclib

usage = '''list systems using kickstart profile'''

description = '''This script lists the system using the specified kickstart profile on the specified Satellite server.'''

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
  help = "path to the parameter file. Default is ~/.sat.conf",
)

parser.add_option(
  "-u",
  "--cobbler-url",
  action = "callback",
  callback = config.parse_url,
  dest = "cobbler_url",
  type = "string",
  default = None,
  help = "Satellite RPC API URL to use",
)
parser.add_option(
  "-a",
  "--cobbler-login",
  action = "callback",
  callback = config.parse_string,
  dest = "cobbler_login",
  type = "string",
  default = None,
  help = "admin account to log in with on Satellite",
)
parser.add_option(
  "-p",
  "--cobbler-password",
  action = "callback",
  callback = config.parse_string,
  dest = "cobbler_password",
  type = "string",
  default = None,
  help = "password belonging to Satellite admin account",
)
parser.add_option(
  "-l",
  "--kickstart-label",
  action = "callback",
  callback = config.parse_string,
  dest = "kickstart_label",
  type = "string",
  default = None,
  help = "kickstart label to export"
)

(options, args) = config.get_conf(parser)

if options.kickstart_label is None:
  parser.error('Error: specify label, -l or --kickstart-label')

# Get session key via auth namespace.
client = xmlrpclib.ServerProxy(options.cobbler_url, verbose=0)
key = client.login(options.cobbler_login, options.cobbler_password)

try:
  systems = client.get_systems()
except xmlrpclib.Fault, e:
  print >> sys.stderr, str(e)

for s in systems:
  m = re.search('([^:]+):([^:]+):([^:]+)', s['profile'])
  if m.group(1) == options.kickstart_label:
    print s['name']

client.logout(key)

