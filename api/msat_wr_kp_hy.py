#!/usr/bin/python

#
# SCRIPT
#   msat_wr_kp_hy.py
# DESCRIPTION
# OPTIONS
# ARGUMENTS
# RETURN
#   0: success.
# DEPENDENCIES
#   You need a Satellite server running to which this client
#   can connect.
# FAILURE
# AUTHORS
#   Date strings made with 'date +"\%Y-\%m-\%d \%H:\%M"'.
#   Allard Berends (AB), 2013-02-24 13:07
#   Gerben Welter (GW),  2013-04-28 23:16
# HISTORY
#   2013-04-28 23:16, GW corrected the calling of other msat
#   scripts in the subprocess calls. The specified command
#   line parameters are now included.
# LICENSE
#   Copyright (C) 2013 Allard Berends
#
#   msat_wr_kp_hy.py is free software; you can redistribute
#   it and/or modify it under the terms of the GNU General
#   Public License as published by the Free Software
#   Foundation; either version 3 of the License, or (at your
#   option) any later version.
#
#   msat_wr_kp_hy.py is distributed in the hope that it will
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
import os
import os.path
import re
import shutil
import stat
import subprocess
import sys
import time
import urlparse
import xmlrpclib

snippetre = re.compile('\$SNIPPET\(\'[^\']+/([^/]+)\'\)')

def scan_for_snippet(snippets, contents, level):
  global save_path
  for line in contents.split('\n'):
    m = snippetre.search(line)
    if m:
      script = 'cs-' + m.group(1) + '.sh'
      script_path = os.path.join(save_path, script)
      f = open(script_path, 'w')
      os.chmod(script_path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)

      subprocess.Popen([satellite_api_dir + '/msat_wr_cs.py', '--snippet-name', m.group(1), '--satellite-url', options.satellite_url , '--satellite-login', options.satellite_login , '--satellite-password', options.satellite_password], stdout=f, stderr=subprocess.STDOUT)
      f.close()
      scan_for_snippet(snippets, snippets[m.group(1)], level + 1)

usage = '''write kickstart hierarchy to script files'''

description = '''This script writes the contents of the specified kickstart profile and connected elements to script files in a directory. If the directory is not specified, it will have the name of the kickstart profile.'''

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
  help = "kickstart label"
)
parser.add_option(
  "-s",
  "--save-path",
  action = "callback",
  callback = config.parse_string,
  dest = "save_path",
  type = "string",
  default = None,
  help = "path to save all information to"
)
(options, args) = config.get_conf(parser)

if options.kickstart_label is None:
  parser.error('specify kickstart label, -l or --kickstart-label. Use list_kickstart_profiles.py to find all kickstart labels.')

satellite_api_dir = os.path.dirname(sys.argv[0])

if options.save_path:
  save_path = os.path.abspath(options.save_path)
else:
  save_path = os.path.abspath(options.kickstart_label)

if os.path.exists(save_path):
  shutil.rmtree(save_path)
os.mkdir(save_path)

# Get session key via auth namespace.
client = xmlrpclib.ServerProxy(options.satellite_url, verbose=0)
key = client.auth.login(options.satellite_login, options.satellite_password)

script = 'kp-' + options.kickstart_label + '.sh'
script_path = os.path.join(save_path, script)
f = open(script_path, 'w')
os.chmod(script_path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)

subprocess.Popen([satellite_api_dir + '/msat_wr_kp.py', '--kickstart-label', options.kickstart_label, '--satellite-url', options.satellite_url , '--satellite-login', options.satellite_login , '--satellite-password', options.satellite_password], stdout=f, stderr=subprocess.STDOUT)
f.close()

try:
  s = client.kickstart.snippet.listCustom(
    key,
  )
except xmlrpclib.Fault, e:
  print >> sys.stderr, str(e)
  print >> sys.stderr, options
  sys.exit(1)

snippets = {}
for i in s:
  snippets[i['name']] = i['contents']

try:
  scripts = client.kickstart.profile.listScripts(
    key,
    options.kickstart_label,
  )
except xmlrpclib.Fault, e:
  print >> sys.stderr, str(e)
  print >> sys.stderr, options
  sys.exit(1)

if len(scripts) > 1:
  print >> sys.stderr, "Error: only one script allowed in kickstart convention"
  sys.exit(1)

if scripts:
  c = scripts[0]['contents']
  scan_for_snippet(snippets, c, 1)

try:
  akeys = client.kickstart.profile.keys.getActivationKeys(
    key,
    options.kickstart_label,
  )
except xmlrpclib.Fault, e:
  print >> sys.stderr, str(e)
  print >> sys.stderr, options
  sys.exit(1)

for a in akeys:
  script = 'ak-' + re.sub('^\d+-', '', a['key']) + '.sh'
  script_path = os.path.join(save_path, script)
  f = open(script_path, 'w')
  os.chmod(script_path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)

  subprocess.Popen([satellite_api_dir + '/msat_wr_ak.py', '--activationkey-label', a['key'], '--satellite-url', options.satellite_url , '--satellite-login', options.satellite_login , '--satellite-password', options.satellite_password], stdout=f, stderr=subprocess.STDOUT)
  f.close()
  try:
    config_channels = client.activationkey.listConfigChannels(
      key,
      a['key'],
    )
  except xmlrpclib.Fault, e:
    continue

  for cc in config_channels:
    script = 'cc-' + cc['label'] + '.sh'
    script_path = os.path.join(save_path, script)
    f = open(script_path, 'w')
    os.chmod(script_path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)

    subprocess.Popen([satellite_api_dir + '/msat_wr_cc.py', '--configchannel-label', cc['label'], '--satellite-url', options.satellite_url , '--satellite-login', options.satellite_login , '--satellite-password', options.satellite_password, '--configchannel-existence', 'yes'], stdout=f, stderr=subprocess.STDOUT)
    f.close()

client.auth.logout(key)
