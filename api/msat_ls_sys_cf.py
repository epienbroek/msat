#!/usr/bin/python

#
# SCRIPT
#   msat_ls_sys_cf.py
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
#   msat_ls_sys_cf.py is free software; you can
#   redistribute it and/or modify it under the terms of the
#   GNU General Public License as published by the Free
#   Software Foundation; either version 3 of the License, or
#   (at your option) any later version.
#
#   msat_ls_sys_cf.py is distributed in the hope
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
import sys
import xmlrpclib

usage = '''list system config files'''

description = '''This script lists the config files of the specified system or all systems.'''

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
  "-v",
  "--satellite-version",
  action = "callback",
  callback = config.parse_string,
  dest = "satellite_version",
  type = "string",
  default = "5.4",
  help = "version of the Satellite API",
)
parser.add_option(
  "-i",
  "--system-id",
  action = "callback", 
  callback = config.parse_int,
  dest = "system_id",
  type = "int",
  default = None,
  help = "system id int"
)

(options, args) = config.get_conf(parser)

# Get session key via auth namespace.
client = xmlrpclib.ServerProxy(options.satellite_url, verbose=0)
key = client.auth.login(options.satellite_login, options.satellite_password)

if options.system_id:
  system_ids = [options.system_id]
else:
  try:
    systems = client.system.listSystems(
      key,
    )
  except xmlrpclib.Fault, e:
    print >> sys.stderr, str(e)
  system_ids = [x['id'] for x in systems]

for i in system_ids:
  try:
    system = client.system.getName(
      key,
      i,
    )
  except xmlrpclib.Fault, e:
    print >> sys.stderr, str(e)
  try:
    files = client.system.config.listFiles(
      key,
      i,
      1
    )
  except xmlrpclib.Fault, e:
    print >> sys.stderr, str(e)
  d = {}
  for f in files:
    try:
      d[f['channel_label']].append(f['path'])
    except KeyError, e:
      d[f['channel_label']] = [f['path']]
  keys = d.keys()
  keys.sort()
  print str(i) + ' (' + system['name'] + ')'
  for k in keys:
    files = d[k]
    files.sort()
    print '  %s' % (k,)
    for f in files:
      print '    %s' % (f,)
  print

client.auth.logout(key)
