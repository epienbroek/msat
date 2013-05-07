#!/usr/bin/python

#
# SCRIPT
#   msat_mk_org.py
# DESCRIPTION
#   Creates a Satellite organization on the Satellite
#   server.
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
#   Allard Berends (AB), 2013-05-07 13:19
# HISTORY
# LICENSE
#   Copyright (C) 2013 Allard Berends
#
#   msat_mk_org.py is free software; you can redistribute it
#   and/or modify it under the terms of the GNU General
#   Public License as published by the Free Software
#   Foundation; either version 3 of the License, or (at your
#   option) any later version.
#
#   msat_mk_org.py is distributed in the hope that it will be
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
  "-n",
  "--org-name",
  action = "callback",
  callback = config.parse_string,
  dest = "org_name",
  type = "string",
  default = None,
  help = "Satellite organization name"
)
parser.add_option(
  "--org-login",
  action = "callback",
  callback = config.parse_string,
  dest = "org_login",
  type = "string",
  default = None,
  help = "Satellite organization admin's login name"
)
parser.add_option(
  "--org-password",
  action = "callback",
  callback = config.parse_string,
  dest = "org_password",
  type = "string",
  default = None,
  help = "Satellite organization admin's password"
)
parser.add_option(
  "--org-prefix",
  action = "callback",
  callback = config.parse_string,
  dest = "org_prefix",
  type = "string",
  default = 'Mr.',
  help = "Admin's prefix, i.e. Dr., Mr., Mrs., Sr., etc."
)
parser.add_option(
  "--org-firstname",
  action = "callback",
  callback = config.parse_string,
  dest = "org_firstname",
  type = "string",
  default = None,
  help = "Admin's first name."
)
parser.add_option(
  "--org-lastname",
  action = "callback",
  callback = config.parse_string,
  dest = "org_lastname",
  type = "string",
  default = None,
  help = "Admin's last name."
)
parser.add_option(
  "--org-email",
  action = "callback",
  callback = config.parse_string,
  dest = "org_email",
  type = "string",
  default = 'root@localhost',
  help = "Satellite organization admin's email address"
)
parser.add_option(
  "--org-pamauth",
  action = "callback",
  callback = config.parse_boolean,
  dest = "org_pamauth",
  type = "string",
  default = False,
  help = "set to yes to use pam authentication"
)
(options, args) = config.get_conf(parser)

if not options.org_name:
  parser.error('Error: specify organization name, -n or --org-name')
if not options.org_login:
  parser.error('Error: specify organization login, --org-login')
if not options.org_password:
  parser.error('Error: specify organization password, --org-password')
if not options.org_firstname:
  parser.error('Error: specify first name, --org-firstname')
if not options.org_lastname:
  parser.error('Error: specify last name, --org-lastname')
if not options.org_email:
  parser.error('Error: specify email, --org-email')

# Get session key via auth namespace.
client = xmlrpclib.ServerProxy(options.satellite_url, verbose=0)
key = client.auth.login(options.satellite_login, options.satellite_password)

try:
  rc = client.org.create(
    key,
    options.org_name,
    options.org_login,
    options.org_password,
    options.org_prefix,
    options.org_firstname,
    options.org_lastname,
    options.org_email,
    options.org_pamauth,
  )
except xmlrpclib.Fault, e:
  print >> sys.stderr, str(e)
  print >> sys.stderr, options
  sys.exit(1)

client.auth.logout(key)
