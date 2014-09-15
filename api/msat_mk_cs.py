#!/usr/bin/python

#
# SCRIPT
#   msat_mk_cs.py
# DESCRIPTION
#   Add a cobbler snipped via the command line. See the
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
#   If you put single quotes around value, but forget to
#   escape embedded single quotes, this script will fail.
#   Escaping works like this:
#   $ echo 'don'"'"'t'
#   don't
#   So ' -> '"'"'
#   Complicated huh?
# AUTHORS
#   Date strings made with 'date +"\%Y-\%m-\%d \%H:\%M"'.
#   Allard Berends (AB), 2013-02-24 13:07
# HISTORY
# LICENSE
#   Copyright (C) 2013 Allard Berends
#
#   msat_mk_cs.py is free software; you can redistribute it
#   and/or modify it under the terms of the GNU General
#   Public License as published by the Free Software
#   Foundation; either version 3 of the License, or (at your
#   option) any later version.
#
#   msat_mk_cs.py is distributed in the hope that it will be
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

usage = '''adds the specified cobbler snippet'''

description = '''This script adds the specified cobbler snipped to the Satellite. If the cobbler snippet does not exist, a new one will be created. If the cobbler snipped already exists, it will be overwritten. So be carefull.'''

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
  "-n",
  "--snippet-name",
  action = "callback",
  callback = config.parse_string,
  dest = "snippet_name",
  type = "string",
  default = None,
  help = "snippet name option"
)
parser.add_option(
  "-c",
  "--snippet-content",
  action = "callback",
  callback = config.parse_file,
  dest = "snippet_content",
  type = "string",
  default = None,
  help = "snippet content option"
)

(options, args) = config.get_conf(parser)

if options.satellite_url is None:
  parser.error('Error: specify URL, -u or --satellite-url')
if options.satellite_login is None:
  parser.error('Error: specify login, -l or --login')
if options.satellite_password is None:
  parser.error('Error: specify password, -p or --password')
if options.snippet_name is None:
  parser.error('Error: specify name, -n or --snippet-name')
if options.snippet_content is None:
  parser.error('Error: specify content, -c or --snippet-content')

# Get session key via auth namespace.
client = xmlrpclib.ServerProxy(options.satellite_url, verbose=0)
key = client.auth.login(options.satellite_login, options.satellite_password)

# create kickstart profile
try:
  rc = client.kickstart.snippet.createOrUpdate(
    key,
    options.snippet_name,
    options.snippet_content,
  )
except xmlrpclib.Fault, e:
  print >> sys.stderr, str(e)
  print >> sys.stderr, options

client.auth.logout(key)
