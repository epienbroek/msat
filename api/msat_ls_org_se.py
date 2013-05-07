#!/usr/bin/python

#
# SCRIPT
#   msat_ls_org_se.py
# DESCRIPTION
#   This script lists the system entitlements for the
#   specified org.
# DEPENDENCIES
#   You need a Satellite server running to which this client
#   can connect.
# FAILURE
# AUTHORS
#   Date strings made with 'date +"\%Y-\%m-\%d \%H:\%M"'.
#   Allard Berends (AB), 2013-05-07 15:02
# HISTORY
# LICENSE
#   Copyright (C) 2013 Allard Berends
# 
#   msat_ls_org_se.py is free software; you can redistribute it
#   and/or modify it under the terms of the GNU General
#   Public License as published by the Free Software
#   Foundation; either version 3 of the License, or (at your
#   option) any later version.
#
#   msat_ls_org_se.py is distributed in the hope that it will be
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
  "--org-header",
  action = "callback",
  callback = config.parse_boolean,
  dest = "org_header",
  type = "string",
  default = 'yes',
  help = "print output header, yes or no",
)
(options, args) = config.get_conf(parser)

if not options.org_number:
  parser.error('Error: specify organization number, -o or --org-number')

# Get session key via auth namespace.
client = xmlrpclib.ServerProxy(options.satellite_url, verbose=0)
key = client.auth.login(options.satellite_login, options.satellite_password)

try:
  se = client.org.listSystemEntitlementsForOrg(
    key,
    options.org_number
  )
except xmlrpclib.Fault, e:
  print >> sys.stderr, str(e)
  sys.exit(1)

if options.org_header:
  print "%-30.30s %11.11s %11.11s %11.11s %11.11s" % ('label', 'free', 'used', 'allocated', 'unallocated')
for i in se:
  print "%-30.30s %11d %11d %11d %11d" % (i['label'], i['free'], i['used'], i['allocated'], i['unallocated'])

client.auth.logout(key)
