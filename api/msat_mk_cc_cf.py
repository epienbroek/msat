#!/usr/bin/python

#
# SCRIPT
#   msat_mk_cc_cf.py
# DESCRIPTION
#   Add a config path via the command line. See the
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
#   Allard Berends (AB),  2013-02-24 13:07
# HISTORY
# LICENSE
#   Copyright (C) 2013 Allard Berends
# 
#   msat_mk_cc_cf.py is free software; you can
#   redistribute it and/or modify it under the terms of the
#   GNU General Public License as published by the Free
#   Software Foundation; either version 3 of the License, or
#   (at your option) any later version.
#
#   msat_mk_cc_cf.py is distributed in the hope that
#   it will be useful, but WITHOUT ANY WARRANTY; without
#   even the implied warranty of MERCHANTABILITY or FITNESS
#   FOR A PARTICULAR PURPOSE. See the GNU General Public
#   License for more details.
#
#   You should have received a copy of the GNU General
#   Public License along with this program; if not, write to
#   the Free Software Foundation, Inc., 59 Temple Place -
#   Suite 330, Boston, MA 02111-1307, USA.
# DESIGN
#

import base64
import config
import optparse
import sys
import xmlrpclib

usage = '''adds or updates a config path to the specified config channel'''

description = '''This script adds or updates a config path to the specified config channel.'''

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
  "--configchannel-label",
  action = "callback", 
  callback = config.parse_string,
  dest = "configchannel_label",
  type = "string",
  default = None,
  help = "config channel label"
)
parser.add_option(
  "--configpath-path",
  action = "callback", 
  callback = config.parse_string,
  dest = "configpath_path",
  type = "string",
  default = None,
  help = "path of file or dir"
)
parser.add_option(
  "-d",
  "--configpath-dir",
  action = "callback", 
  callback = config.parse_boolean,
  dest = "configpath_dir",
  type = "string",
  default = False,
  help = "path is directory"
)
parser.add_option(
  "-c",
  "--configpath-content",
  action = "callback", 
  callback = config.parse_string,
  dest = "configpath_content",
  type = "string",
  default = None,
  help = "path to content of a config file"
)
parser.add_option(
  "--configpath-user",
  action = "callback", 
  callback = config.parse_string,
  dest = "configpath_user",
  type = "string",
  default = None,
  help = "user of a config file"
)
parser.add_option(
  "-g",
  "--configpath-group",
  action = "callback", 
  callback = config.parse_string,
  dest = "configpath_group",
  type = "string",
  default = None,
  help = "group of a config file"
)
parser.add_option(
  "--configpath-permissions",
  action = "callback", 
  callback = config.parse_string,
  dest = "configpath_permissions",
  type = "string",
  default = None,
  help = "permissions of a path"
)
parser.add_option(
  "-s",
  "--configpath-startdelimiter",
  action = "callback", 
  callback = config.parse_string,
  dest = "configpath_startdelimiter",
  type = "string",
  default = '{|',
  help = "start-delimiter of a macro in a config file, [default: \'%default\']"
)
parser.add_option(
  "-e",
  "--configpath-enddelimiter",
  action = "callback", 
  callback = config.parse_string,
  dest = "configpath_enddelimiter",
  type = "string",
  default = '|}',
  help = "end-delimter of a macro in a config file, [default: \'%default\']"
)
(options, args) = config.get_conf(parser)

if options.configchannel_label is None:
  parser.error('Error: specify label, -l or --configchannel-label')
if options.configpath_path is None:
  parser.error('Error: specify path, -p or --configpath-path')
if not options.configpath_dir and options.configpath_content is None:
  parser.error('Error: specify config file path, -c or --configpath-content')
if options.configpath_user is None:
  parser.error('Error: specify user, -u or --configpath-user')
if options.configpath_group is None:
  parser.error('Error: specify group, -g or --configpath-group')
if options.configpath_permissions is None:
  parser.error('Error: specify file permissions, -f or --configpath-permissions')

# Get session key via auth namespace.
client = xmlrpclib.ServerProxy(options.satellite_url, verbose=0)
key = client.auth.login(options.satellite_login, options.satellite_password)

content = 'NULL'
if not options.configpath_dir:
  if options.configpath_content == '-':
    f = sys.stdin
  else:
    try:
      f = open(options.configpath_content, 'r')
    except IOError, e:
      print >> sys.stderr, str(e)
      print >> sys.stderr, options.configpath_content
      sys.exit(1)
  content = ''.join(f.readlines())

# Note, always use Base64 encoding. Otherwise the
# end-of-line at the end of the config file is gone.
# iptables, motd, etc. break.
path_info = {
  'owner':                 options.configpath_user,
  'group':                 options.configpath_group,
  'permissions':           options.configpath_permissions,
}
if not options.configpath_dir:
  path_info['macro-start-delimiter'] = options.configpath_startdelimiter
  path_info['macro-end-delimiter']   = options.configpath_enddelimiter

if options.satellite_version == '5.5':
  if not options.configpath_dir:
    path_info['contents']       = base64.standard_b64encode(content)
    path_info['contents_enc64'] = True
    path_info['binary']         = False
  path_info['revision']       = ''
else:
  if not options.configpath_dir:
    path_info['contents'] = xmlrpclib.Binary(content)

try:
  rc = client.configchannel.createOrUpdatePath(
    key, 
    options.configchannel_label,
    options.configpath_path,
    options.configpath_dir,
    path_info
  )
except xmlrpclib.Fault, e:
  print >> sys.stderr, str(e)
  print >> sys.stderr, options
  sys.exit(1)

client.auth.logout(key)
