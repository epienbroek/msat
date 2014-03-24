#!/usr/bin/python

#
# SCRIPT
#   msat_mk_ag.py
# DESCRIPTION
#   Associates a GPG key ID to a provider name.
# OPTIONS
#   See the optparse code. parser.add_option statements.
# ARGUMENTS
#   None.
# RETURN
#   0: success.
# DEPENDENCIES
#   You need a Satellite server running to which this client
#   can connect and requires Satellite Admin privileges.
# FAILURE
# AUTHORS
#   Date strings made with 'date +"\%Y-\%m-\%d \%H:\%M"'.
#   Gerben Welter (GW), 2014-03-24 12:47
# HISTORY
# LICENSE
#   Copyright (C) 2013 Gerben Welter
#
#   msat_mk_ag.py is free software; you can redistribute it
#   and/or modify it under the terms of the GNU General
#   Public License as published by the Free Software
#   Foundation; either version 3 of the License, or (at your
#   option) any later version.
#
#   msat_mk_ag.py is distributed in the hope that it will be
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

usage = '''Associate GPG key ID to provider name'''

description = '''This script creates an association between the GPG key ID and the Content Provider name in Satellite.'''

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
  "-g",
  "--gpg-keyid",
  action = "callback",
  callback = config.parse_string,
  dest = "gpg_keyid",
  type = "string",
  default = None,
  help = "GPG key ID"
)
parser.add_option(
  "-P",
  "--provider-name",
  action = "callback",
  callback = config.parse_string,
  dest = "gpg_provider",
  type = "string",
  default = None,
  help = "GPG Provider name"
)

(options, args) = config.get_conf(parser)

if not options.gpg_keyid:
  parser.error('Error: specify GPG fingerprint, -g or --gpg-keyid')
if not options.gpg_provider:
  parser.error('Error: specify GPG provider name, -P or --gpg-provider')

# Get session key via auth namespace.
client = xmlrpclib.ServerProxy(options.satellite_url, verbose=0)
key = client.auth.login(options.satellite_login, options.satellite_password)

try:
  rc = client.packages.provider.associateKey(
    key,
    options.gpg_provider,
    options.gpg_keyid,
    "gpg",
  )
except xmlrpclib.Fault, e:
  print >> sys.stderr, str(e)
  print >> sys.stderr, options
  sys.exit(1)

client.auth.logout(key)
