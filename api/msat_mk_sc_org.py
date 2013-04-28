#!/usr/bin/python

#
# SCRIPT
#   msat_mk_sc_org.py
# DESCRIPTION
# DEPENDENCIES
#   You need a Satellite server running to which this client
#   can connect.
# FAILURE
# AUTHORS
#   Date strings made with 'date +"\%Y-\%m-\%d \%H:\%M"'.
#   Allard Berends (AB),  2013-02-24 13:07
# HISTORY
# LICENSE
#   Copyright (C) 2013 Allard Berends
# 
#   msat_mk_sc_org.py is free software; you can redistribute it
#   and/or modify it under the terms of the GNU General
#   Public License as published by the Free Software
#   Foundation; either version 3 of the License, or (at your
#   option) any later version.
#
#   msat_mk_sc_org.py is distributed in the hope that it will be
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

usage = '''make software channel shared to org'''

description = '''This script makes the specified software channel shared at the specified level to the specified Satellite organization.'''

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
  "-l",
  "--softwarechannel-label",
  action = "callback",
  callback = config.parse_string,
  dest = "softwarechannel_label",
  type = "string",
  default = None,
  help = "softwarechannel label"
)
parser.add_option(
  "-o",
  "--satellite-org",
  action = "callback",
  callback = config.parse_int,
  dest = "satellite_org",
  type = "int",
  default = None,
  help = "satellite org id (int)"
)
parser.add_option(
  "-s",
  "--satellite-access",
  action = "callback",
  callback = config.parse_string,
  dest = "satellite_access",
  type = "string",
  default = 'protected',
  help = "org access level, public, private, or protected"
)
parser.add_option(
  "-t",
  "--satellite-trust",
  action = "callback",
  callback = config.parse_boolean,
  dest = "satellite_trust",
  type = "string",
  default = 'yes',
  help = "add trust to org? specify yes, otherwise no"
)
(options, args) = config.get_conf(parser)

# Get session key via auth namespace.
client = xmlrpclib.ServerProxy(options.satellite_url, verbose=0)
key = client.auth.login(options.satellite_login, options.satellite_password)

if options.softwarechannel_label is None:
  parser.error('Error: specify label, -l or --softwarechannel-label')

if options.satellite_org is None:
  parser.error('Error: specify org, -o or --satellite-org')

if options.satellite_trust:
  try:
    client.channel.access.setOrgSharing(
      key,
      options.softwarechannel_label,
      options.satellite_access,
    )
  except xmlrpclib.Fault, e:
    print >> sys.stderr, str(e)
    print >> sys.stderr, options.softwarechannel_label, options.satellite_access
    sys.exit(1)
  try:
    orgs = client.channel.org.enableAccess(
      key,
      options.softwarechannel_label,
      options.satellite_org,
    )
  except xmlrpclib.Fault, e:
    print >> sys.stderr, str(e)
    print >> sys.stderr, options.softwarechannel_label, options.satellite_org
    sys.exit(1)
else:
  try:
    orgs = client.channel.org.disableAccess(
      key,
      options.softwarechannel_label,
      options.satellite_org,
    )
  except xmlrpclib.Fault, e:
    print >> sys.stderr, str(e)
    print >> sys.stderr, options.softwarechannel_label, options.satellite_org
    sys.exit(1)

client.auth.logout(key)
