#!/usr/bin/python

#
# SCRIPT
#   msat_wr_er.py
# DESCRIPTION
# DEPENDENCIES
#   You need a Satellite server running to which this client
#   can connect.
# FAILURE
# AUTHORS
#   Date strings made with 'date +"\%Y-\%m-\%d \%H:\%M"'.
#   Gerben Welter (GW),  2014-09-26 20:45
# HISTORY
# LICENSE
#   Copyright (C) 2014 Gerben Welter
#
#   msat_wr_er.py is free software; you can redistribute it
#   and/or modify it under the terms of the GNU General
#   Public License as published by the Free Software
#   Foundation; either version 3 of the License, or (at your
#   option) any later version.
#
#   msat_wr_er.py is distributed in the hope that it will be
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
import os
import re
import subprocess
import sys
import xmlrpclib

usage = '''add packages from erratum to software channel'''

description = '''This script filters a list of the packages in the erratum applicable to the specified errata software channel.'''

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
  "-e",
  "--erratum-label",
  action = "callback",
  callback = config.parse_string,
  dest = "erratum_label",
  type = "string",
  default = None,
  help = "erratum label"
)
parser.add_option(
  "-l",
  "--destination-channel",
  action = "callback",
  callback = config.parse_string,
  dest = "destination_channel",
  type = "string",
  default = None,
  help = "errata channel to push applicable packages from erratum to"
)

(options, args) = config.get_conf(parser)

if options.erratum_label is None:
	    parser.error('specify erratum label, -e or --erratum-label.')
if options.destination_channel is None:
	  parser.error('specify destination channel, -l or --destination-channel. Use msat_ls_sc.py to find all software channels.')

satellite_api_dir = os.path.dirname(sys.argv[0])

# Get session key via auth namespace.
client = xmlrpclib.ServerProxy(options.satellite_url, verbose=0)
key = client.auth.login(options.satellite_login, options.satellite_password)

try:
  erratum = client.errata.listPackages(
    key,
    options.erratum_label,
  )
except xmlrpclib.Fault, e:
  print >> sys.stderr, str(e)
  print >> sys.stderr, erratum

client.auth.logout(key)

# GW: Split the destination channel to filter out the type of channel and
#     the major version to build a regex

f = options.destination_channel.split("-")
type = f[3]
major_version = f[5].split("u")[0]

reObj = re.compile('.*%s-.*%s' % (type, major_version))

# GW: Loop through the erratum and go through an inner loop to match the
#     providing_channels key to the regex. Using a set() to build a hash
#     containing only unique package id's. Finally join the hash in a string
#     that can be used as an argument for msat_mk_sc_rpms.py.
matching_ids=set()
for i in erratum:
  for j in i['providing_channels']:
    if bool(reObj.match(j)):
      matching_ids.update([i['id']])
list=','.join(map(str, matching_ids))

# GW: Finally call msat_mk_sc_rpms.py to add the packages to the specified errata channel.
subprocess.Popen([satellite_api_dir + '/msat_mk_sc_rpms.py', '--softwarechannel-label', options.destination_channel, '--satellite-url', options.satellite_url , '--satellite-login', options.satellite_login , '--satellite-password', options.satellite_password, '--rpm-ids', list])

