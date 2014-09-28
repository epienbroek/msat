#!/usr/bin/python

#
# SCRIPT
#   msat_wr_sc_rpms.py
# DESCRIPTION
#   The purpose of this script is to explore the different
#   API methods from python towards the Satellite server.
#
#   The information about the api can be fount at:
#   http://docs.redhat.com/docs/en-US/Red_Hat_Network_Satellite/5.3/html/API_Overview/index.html
#   It does not provide any specific other functional
#   purpose.  The API namespaces are:
#   * api
#   * auth
#   * channel
#   * channel.software
#   * errata
#   * packages
#   * proxy
#   * satellite
#   * systemgroup
#   * system
#   * user

# DEPENDENCIES
#   You need a Satellite server running to which this client
#   can connect.
# FAILURE
# AUTHORS
#   Date strings made with 'date +"\%Y-\%m-\%d \%H:\%M"'.
#   Allard Berends (AB),  2013-02-24 13:07
# HISTORY
#   Allard Berends (AB),  2013-02-24 13:07 added creation of
#                         Satellite software channel.
#
# LICENSE
#   Copyright (C) 2013 Allard Berends
#g
#   msat_wr_sc_rpms.py is free software; you
#   can redistribute it and/or modify it under the terms of
#   the GNU General Public License as published by the Free
#   Software Foundation; either version 3 of the License, or
#   (at your option) any later version.
#
#   msat_wr_sc_rpms.py is distributed in the
#   hope that it will be useful, but WITHOUT ANY WARRANTY;
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
import os.path
import shutil
import sys
import xmlrpclib

usage = '''list kickstart profiles'''

description = '''This script lists the kickstart profiles on the specified Satellite server.'''

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
  "--satellite-rpmpath",
  action = "callback",
  callback = config.parse_string,
  dest = "satellite_rpmpath",
  type = "string",
  default = None,
  help = "Satellite rpm path",
)

parser.add_option(
  "-l",
  "--softwarechannel-label",
  action = "callback",g
  callback = config.parse_string,
  dest = "softwarechannel_label",
  type = "string",
  default = None,
  help = "softwarechannel label"
)
parser.add_option(
  "-e",
  "--softwarechannel-export",
  action = "callback",g
  callback = config.parse_string,
  dest = "softwarechannel_export",
  type = "string",
  default = None,
  help = "export directory"
)
(options, args) = config.get_conf(parser)

if options.softwarechannel_label is None:
  parser.error('Error: specify label, -l or --softwarechannel-label')
if options.softwarechannel_export is None:
  parser.error('Error: specify export, -e or --softwarechannel-export')

# Get session key via auth namespace.
client = xmlrpclib.ServerProxy(options.satellite_url, verbose=0)
key = client.auth.login(options.satellite_login, options.satellite_password)

try:
  list = client.channel.software.listAllPackages(
    key,
    options.softwarechannel_label,
  )
except xmlrpclib.Fault, e:
  print >> sys.stderr, str(e)
  print >> sys.stderr, options.softwarechannel_label
  sys.exit(1)

export_path = os.path.join(options.softwarechannel_export, options.softwarechannel_label)
if os.path.exists(export_path):
  shutil.rmtree(export_path)
os.makedirs(export_path)

for pkg in list:
  id = pkg.get('id')

  try:
    details = client.packages.getDetails(
      key,
      id,
    )
  except xmlrpclib.Fault, e:
    print >> sys.stderr, str(e)
    print >> sys.stderr, id

  shutil.copy(os.path.join(options.satellite_rpmpath, details['path']),
              export_path)

client.auth.logout(key)

