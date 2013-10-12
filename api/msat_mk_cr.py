#!/usr/bin/python

#
# SCRIPT
#   msat_mk_cr.py
# DESCRIPTION
#   Script to add GPG key to Satellite org.
# DEPENDENCIES
#   You need a Satellite server running to which this client
#   can connect.
# FAILURE
# AUTHORS
#   Date strings made with 'date +"\%Y-\%m-\%d \%H:\%M"'.
#   Allard Berends (AB), 2013-05-22 18:24
# HISTORY
# LICENSE
#   Copyright (C) 2013 Allard Berends
# 
#   msat_mk_cr.py is free software; you can
#   redistribute it and/or modify it under the terms of the
#   GNU General Public License as published by the Free
#   Software Foundation; either version 3 of the License, or
#   (at your option) any later version.
#
#   msat_mk_cr.py is distributed in the hope
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

usage = '''add cryptographic key to org'''

description = '''This script adds the cryptographic key to the specified Satellite org.'''

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
  "-d",
  "--key-description",
  action = "callback", 
  callback = config.parse_string,
  dest = "key_description",
  type = "string",
  default = None,
  help = "name of the key, used in kp"
)
parser.add_option(
  "-t",
  "--key-type",
  action = "callback", 
  callback = config.parse_string,
  dest = "key_type",
  type = "string",
  default = None,
  help = "GPG or SSL"
)
parser.add_option(
  "-c",
  "--key-content",
  action = "callback", 
  callback = config.parse_string,
  dest = "key_content",
  type = "string",
  default = None,
  help = "path to content (base64) of key file"
)

(options, args) = config.get_conf(parser)

if options.key_description is None:
  parser.error('Error: specify description, -d or --key-description')
if options.key_type is None:
  parser.error('Error: specify type, -t or --key-type, GPG or SSL')
if options.key_content is None:
  parser.error('Error: specify path, -c or --key-content')

# Get session key via auth namespace.
client = xmlrpclib.ServerProxy(options.satellite_url, verbose=0)
key = client.auth.login(options.satellite_login, options.satellite_password)

content = 'NULL'
if options.key_content == '-':
  f = sys.stdin
else:
  try:
    f = open(options.key_content, 'r')
  except IOError, e:
    print >> sys.stderr, str(e)
    print >> sys.stderr, options.key_content
    sys.exit(1)
content = ''.join(f.readlines())

try:
  ret = client.kickstart.keys.create(
    key,
    options.key_description,
    options.key_type,
    content,
  )
except xmlrpclib.Fault, e:
  print >> sys.stderr, str(e)
  sys.exit(1)

client.auth.logout(key)
