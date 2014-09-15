#!/usr/bin/python

#
# SCRIPT
#   msat_ls_cc_ak.py
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
#   msat_ls_cc_ak.py is free software; you can redistribute
#   it and/or modify it under the terms of the GNU General
#   Public License as published by the Free Software
#   Foundation; either version 3 of the License, or (at your
#   option) any later version.
#
#   msat_ls_cc_ak.py is distributed in the hope that it will
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
usage = '''list activation keys referencing config channel'''

description = '''This script lists the activation keys that reference specified config channel.'''

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
  "--configchannel-label",
  action = "callback",
  callback = config.parse_string,
  dest = "configchannel_label",
  type = "string",
  default = None,
  help = "configchannel label"
)
(options, args) = config.get_conf(parser)

if options.configchannel_label is None:
  parser.error('Error: specify label, -l or --configchannel-label')

# Get session key via auth namespace.
client = xmlrpclib.ServerProxy(options.satellite_url, verbose=0)
key = client.auth.login(options.satellite_login, options.satellite_password)

references = []
try:
  activation_keys = client.activationkey.listActivationKeys(
    key,
  )
except xmlrpclib.Fault, e:
  print >> sys.stderr, str(e)

for i in activation_keys:
  try:
    config_channels = client.activationkey.listConfigChannels(
      key,
      i['key']
    )
  except xmlrpclib.Fault, e:
    print >> sys.stderr, str(e)
    print >> sys.stderr, options.activationkey_label
    sys.exit(1)

  for cc in config_channels:
    if cc.get('label') == options.configchannel_label:
      print i['key']
      break

client.auth.logout(key)
