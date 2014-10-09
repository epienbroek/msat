#!/usr/bin/python

#
# SCRIPT
#   msat_ls_ak_cc.py
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
#   msat_ls_ak_cc.py is free software; you can redistribute
#   it and/or modify it under the terms of the GNU General
#   Public License as published by the Free Software
#   Foundation; either version 3 of the License, or (at your
#   option) any later version.
#
#   msat_ls_ak_cc.py is distributed in the hope that it will
#   be useful, but WITHOUT ANY WARRANTY; without even the
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

# Standard layout for the help:
# * usage
# * desctiption
# * options help
# * epilog

# Standard layout of man page:
# * name (%prog)
# * synopsis (usage)
# * copyright (...)
# * description (description)
# * options (options help)
# * other (epilog)
usage = '''list config channels of activation key'''

description = '''This script lists the config channels attached to an activation key.  If the activation key does not exist, an error will be given and a dump of the used parameters.'''

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
  help = "Path to the parameter file",
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
  help = "Admin account to log in with on Satellite",
)
parser.add_option(
  "-p",
  "--satellite-password",
  action = "callback",
  callback = config.parse_string,
  dest = "satellite_password",
  type = "string",
  default = None,
  help = "Password belonging to Satellite admin account",
)

parser.add_option(
  "-l",
  "--activationkey-label",
  action = "callback",
  callback = config.parse_string,
  dest = "activationkey_label",
  type = "string",
  default = None,
  help = "Activationkey label"
)
(options, args) = config.get_conf(parser)

if options.activationkey_label is None:
  parser.error('Error: specify label, -l or --activationkey-label')

# Get session key via auth namespace.
client = xmlrpclib.ServerProxy(options.satellite_url, verbose=0)
key = client.auth.login(options.satellite_login, options.satellite_password)

try:
  config_channels = client.activationkey.listConfigChannels(
    key,
    options.activationkey_label,
  )
except xmlrpclib.Fault, e:
  print >> sys.stderr, str(e)
  print >> sys.stderr, options.activationkey_label
  sys.exit(1)

for cc in config_channels:
  print cc.get('label')

client.auth.logout(key)
