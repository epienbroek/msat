#!/usr/bin/python

#
# SCRIPT
#   msat_ls_kp_hy.py
# DESCRIPTION
#   This script lists the Cobbler snippets referenced from
#   the script, scpecified by the kickstart profile.
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
#   msat_ls_kp_hy.py is free software; you can redistribute
#   it and/or modify it under the terms of the GNU General
#   Public License as published by the Free Software
#   Foundation; either version 3 of the License, or (at your
#   option) any later version.
#
#   msat_ls_kp_hy.py is distributed in the hope that it will
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
import re
import sys
import xmlrpclib

snippetre = re.compile('\$SNIPPET\(\'[^\']+/([^/]+)\'\)')

def scan_for_snippet(snippets, contents, level):
  for line in contents.split('\n'):
    m = snippetre.search(line)
    if m:
      print 'cs %s%s' % ('  ' * level, m.group(1))
      scan_for_snippet(snippets, snippets[m.group(1)], level + 1)

def print_cc(cc, level):
  print 'cc %s%s' % ('  ' * level, cc)
  try:
    config_files = client.configchannel.listFiles(
      key,
      cc
    )
  except xmlrpclib.Fault, e:
    print >> sys.stderr, str(e)
    print >> sys.stderr, cc
    sys.exit(1)

  level += 1
  for f in config_files:
    k = f.get('path')
    print 'cf %s%s' % ('  ' * level, k)

def print_ak(ak, level):
  print 'ak %s%s' % ('  ' * level, ak)
  try:
    config_channels = client.activationkey.listConfigChannels(
      key,
      ak
    )
  except xmlrpclib.Fault, e:
    print >> sys.stderr, str(e)
    print >> sys.stderr, ak
    sys.exit(1)

  for cc in config_channels:
    print_cc(cc.get('label'), level + 1)

usage = '''hierarchically list data elements of kickstart profile'''

description = '''This script lists the cobbler snippets, activation keys, config channels and config files of the specified kickstart profile on the specified Satellite server hierarchically.'''

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
  "--kickstart-label",
  action = "callback", 
  callback = config.parse_string,
  dest = "kickstart_label",
  type = "string",
  default = None,
  help = "kickstart label to export"
)
(options, args) = config.get_conf(parser)

if options.kickstart_label is None:
  parser.error('Error: specify label, -l or --kickstart-label')

# Get session key via auth namespace.
client = xmlrpclib.ServerProxy(options.satellite_url, verbose=0)
key = client.auth.login(options.satellite_login, options.satellite_password)

level = 0
print 'kp %s%s' % ('  ' * level, options.kickstart_label)

try:
  s = client.kickstart.snippet.listCustom(
    key,
  )
except xmlrpclib.Fault, e:
  print >> sys.stderr, str(e)
  print >> sys.stderr, options

snippets = {}
for i in s:
  snippets[i['name']] = i['contents']

# Get script: Systems > Kickstart > Profiles > Scripts >
# Script 1
try:
  scripts = client.kickstart.profile.listScripts(
    key,
    options.kickstart_label,
  )
except xmlrpclib.Fault, e:
  print >> sys.stderr, str(e)
  print >> sys.stderr, options

if len(scripts) > 1:
  print >> sys.stderr, "Error: only one script allowed in kickstart convention"
  sys.exit(1)

c = scripts[0]['contents']
scan_for_snippet(snippets, c, 1)

try:
  activation_keys = client.kickstart.profile.keys.getActivationKeys(
    key,
    options.kickstart_label,
  )
except xmlrpclib.Fault, e:
  print >> sys.stderr, str(e)
  print >> sys.stderr, options.kickstart_label
  sys.exit(1)

for ak in activation_keys:
  k = ak.get('key')
  print_ak(k, 1)

client.auth.logout(key)
