#!/usr/bin/python

#
# SCRIPT
#   msat_rm_sys.py
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
#   msat_rm_sys.py is free software; you can redistribute
#   it and/or modify it under the terms of the GNU General
#   Public License as published by the Free Software
#   Foundation; either version 3 of the License, or (at your
#   option) any later version.
#
#   msat_rm_sys.py is distributed in the hope that it
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

usage = '''remove system'''

description = '''This script removes the specified system from the Satellite server. The system is removed based on its name. If multiple system instances with the same name exist on the Satellite server, all are removed.'''

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
  "--system-name",
  action = "callback",
  callback = config.parse_string,
  dest = "system_name",
  type = "string",
  default = None,
  help = "system name string"
)
(options, args) = config.get_conf(parser)

# Get session key via auth namespace.
client = xmlrpclib.ServerProxy(options.satellite_url, verbose=0)
key = client.auth.login(options.satellite_login, options.satellite_password)

if not options.system_name:
  print >> sys.stderr, 'ERROR: must specify system name, -n or --system-name'
  sys.exit(1)

try:
  systems = client.system.listSystems(
    key,
  )
except xmlrpclib.Fault, e:
  print >> sys.stderr, str(e)
  sys.exit(1)

ids = []
for i in systems:
  try:
    system = client.system.getName(
      key,
      i['id'],
    )
  except xmlrpclib.Fault, e:
    print >> sys.stderr, str(e)
    sys.exit(1)
  if system['name'] == options.system_name:
    ids.append(system['id'])

print 'Removing the following systems (ID\'s):'
for i in ids:
  print i

try:
  client.system.deleteSystems(
    key,
    ids
  )
except xmlrpclib.Fault, e:
  print >> sys.stderr, str(e)
  sys.exit(1)

client.auth.logout(key)
