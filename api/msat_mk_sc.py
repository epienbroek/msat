#!/usr/bin/python

#
# SCRIPT
#   msat_mk_sc.py
# DESCRIPTION
#   Add a software channel via the command line. See the
#   usage string for more help.
# OPTIONS
#   See the optparse code. parser.add_option statements.
# ARGUMENTS
#   None.
# RETURN
#   0: success.
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
#   msat_mk_sc.py is free software; you can redistribute it
#   and/or modify it under the terms of the GNU General
#   Public License as published by the Free Software
#   Foundation; either version 3 of the License, or (at your
#   option) any later version.
#
#   msat_mk_sc.py is distributed in the hope that it will be
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

usage = '''create software channel'''

description = '''This script creates the specified software channel.'''

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
  "-l",
  "--softwarechannel-label",
  action = "callback", 
  callback = config.parse_string,
  dest = "softwarechannel_label",
  type = "string",
  default = None,
  help = "config channel label"
)
parser.add_option(
  "-n",
  "--softwarechannel-name",
  action = "callback", 
  callback = config.parse_string,
  dest = "softwarechannel_name",
  type = "string",
  default = None,
  help = "config channel name"
)
parser.add_option(
  "-s",
  "--softwarechannel-summary",
  action = "callback", 
  callback = config.parse_string,
  dest = "softwarechannel_summary",
  type = "string",
  default = None,
  help = "config channel summary"
)
parser.add_option(
  "--softwarechannel-arch",
  action = "callback", 
  callback = config.parse_string,
  dest = "softwarechannel_arch",
  type = "string",
  default = None,
  help = "software channel arch, e.g. channel-x86_64"
)
parser.add_option(
  "--softwarechannel-parent",
  action = "callback", 
  callback = config.parse_string,
  dest = "softwarechannel_parent",
  type = "string",
  default = '',
  help = "config channel parent"
)
(options, args) = config.get_conf(parser)

if options.softwarechannel_label is None:
  parser.error('Error: specify label, -l or --softwarechannel-label')
if options.softwarechannel_name is None:
  parser.error('Error: specify name, -n or --softwarechannel-name')
if options.softwarechannel_summary is None:
  parser.error('Error: specify summary, -s or --softwarechannel-summary')
if options.softwarechannel_arch is None:
  parser.error('Error: specify arch, --softwarechannel-arch')
if options.softwarechannel_parent is None:
  parser.error('Error: specify parent, --softwarechannel-parent')

# Get session key via auth namespace.
client = xmlrpclib.ServerProxy(options.satellite_url, verbose=0)
key = client.auth.login(options.satellite_login, options.satellite_password)

try:
  rc = client.channel.software.create(
    key, 
    options.softwarechannel_label,
    options.softwarechannel_name,
    options.softwarechannel_summary,
    options.softwarechannel_arch,
    options.softwarechannel_parent,
  )
except xmlrpclib.Fault, e:
  print >> sys.stderr, str(e)
  print >> sys.stderr, options

client.auth.logout(key)
