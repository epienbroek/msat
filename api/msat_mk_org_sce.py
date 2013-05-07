#!/usr/bin/python

#
# SCRIPT
#   msat_mk_org_sce.py
# DESCRIPTION
#   This script lists the software channel entitlements for
#   the specified org.
# DEPENDENCIES
#   You need a Satellite server running to which this client
#   can connect.
# FAILURE
# AUTHORS
#   Date strings made with 'date +"\%Y-\%m-\%d \%H:\%M"'.
#   Allard Berends (AB), 2013-05-07 15:30
# HISTORY
# LICENSE
#   Copyright (C) 2013 Allard Berends
# 
#   msat_mk_org_sce.py is free software; you can redistribute it
#   and/or modify it under the terms of the GNU General
#   Public License as published by the Free Software
#   Foundation; either version 3 of the License, or (at your
#   option) any later version.
#
#   msat_mk_org_sce.py is distributed in the hope that it will be
#   useful, but WITHOUT ANY WARRANTY; without even the
#   implied warranty of MERCHANTABILITY or FITNESS FOR A
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

usage = '''list system entitlements of org'''

description = '''This script lists the system entitlements of the specified organization.'''

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
  "-o",
  "--org-number",
  action = "callback",
  callback = config.parse_int,
  dest = "org_number",
  type = "int",
  default = None,
  help = "Satellite organization number. Use msat_ls_orgs.py to find org numbers",
)
parser.add_option(
  "--org-sce",
  action = "callback",
  callback = config.parse_string,
  dest = "org_sce",
  type = "string",
  default = None,
  help = "comma separated list of arg=value pairs of software channel entitlements",
)
(options, args) = config.get_conf(parser)

if not options.org_number:
  parser.error('Error: specify organization number, -o or --org-number')
if not options.org_sce:
  parser.error('Error: specify software channel entitlements arg=value pairs, --org-sce')

# Get session key via auth namespace.
client = xmlrpclib.ServerProxy(options.satellite_url, verbose=0)
key = client.auth.login(options.satellite_login, options.satellite_password)

sces = options.org_sce.split(',')

for i in sces:
  arg, val = i.split('=')
  try:
    se = client.org.setSoftwareEntitlements(
      key,
      options.org_number,
      arg,
      int(val),
    )
  except xmlrpclib.Fault, e:
    print >> sys.stderr, str(e)
    sys.exit(1)

client.auth.logout(key)
