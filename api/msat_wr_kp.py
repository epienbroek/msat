#!/usr/bin/python

#
# SCRIPT
#   msat_wr_kp.py
# DESCRIPTION
# OPTIONS
# ARGUMENTS
# RETURN
#   0: success.
# DEPENDENCIES
#   You need a Satellite server running to which this client
#   can connect.
# FAILURE
#   If you manually edit the result of this script and don't
#   escape the single quotes, then the result script will
#   fail. Escaping works like this:
#   $ echo 'don'"'"'t'
#   don't
#   So ' -> '"'"'
#   Complicated huh?
# AUTHORS
#   Date strings made with 'date +"\%Y-\%m-\%d \%H:\%M"'.
#   Allard Berends (AB), 2013-02-24 13:07
#   Gerben Welter (GW),  2013-04-28 23:17
# HISTORY
#   2013-04-28 23:17, GW corrected some of the command line
#   parameters.
# LICENSE
#   Copyright (C) 2013 Allard Berends
# 
#   msat_wr_kp.py is free software; you can
#   redistribute it and/or modify it under the terms of the
#   GNU General Public License as published by the Free
#   Software Foundation; either version 3 of the License, or
#   (at your option) any later version.
#
#   msat_wr_kp.py is distributed in the hope
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
import re
import sys
import time
import urlparse
import xmlrpclib

def escape_quote(s):
  # Remove nasty long dash u'u2013' with --
  s = re.sub(u'(?ms)[\u2013\u00ad]', '--', s)
  s = s.encode('ascii')
  e = re.sub('(?ms)\'', '\'"\'"\'', s)
  return e

usage = '''writes the kickstart profile creation script to stdout'''

description = '''This script writes the kickstart creation script of the specified kickstart profile to stdout. The script can be used to recreate the kickstart profile.'''

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
  "--kickstart-label",
  action = "callback", 
  callback = config.parse_string,
  dest = "kickstart_label",
  type = "string",
  default = None,
  help = "kickstart label"
)
parser.add_option(
  "-e",
  "--kickstart-existence",
  action = "callback",
  callback = config.parse_boolean,
  dest = "kickstart_existence",
  type = "string",
  default = None,
  help = "test for kickstart existence in regeneration script"
)
(options, args) = config.get_conf(parser)
if options.satellite_url is None:
  parser.error('Error: specify URL, -u or --satellite-url')
if options.satellite_login is None:
  parser.error('Error: specify login, -a or --satellite-login')
if options.satellite_password is None:
  parser.error('Error: specify password, -p or --satellite-password')
if options.kickstart_label is None:
  parser.error('specify kickstart label, -l or --kickstart-label. Use list_kickstart_profiles.py to find all kickstart labels.')

# Get session key via auth namespace.
client = xmlrpclib.ServerProxy(options.satellite_url, verbose=0)
key = client.auth.login(options.satellite_login, options.satellite_password)

script = 'kp-' + options.kickstart_label + '.sh'
t = time.strftime("%Y-%m-%d %H:%M", time.localtime())
y = time.strftime("%Y", time.localtime())
print '''#!/bin/bash
#
# SCRIPT
#   ''' + script + '''
# DESCRIPTION
#   This script creates the ''' + options.kickstart_label + '''
#   kickstart profile.
# ARGUMENTS
#   None.
# RETURN
#   0: success.
# DEPENDENCIES
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
#   Allard Berends (AB), ''' + t + '''
# HISTORY
# LICENSE
#   Copyright (C) ''' + y + ''' Allard Berends
# 
#   ''' + script + ''' is free software; you can
#   redistribute it and/or modify it under the terms of the
#   GNU General Public License as published by the Free
#   Software Foundation; either version 3 of the License, or
#   (at your option) any later version.
#
#   ''' + script + ''' is distributed in the hope
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

'''

if options.kickstart_existence:
  print  '''if [ -n "$(msat_ls_kp.py | /bin/grep '^%s$')" ]; then
  /bin/echo "INFO: %s already exists! Bailing out."
  exit 0
fi
''' % (options.kickstart_label, options.kickstart_label)

print "ORGNUM=$(msat_ls_org.py)"
print
print "SATELLITE=$(msat_ls_sn.py)"
print '''
msat_mk_kp.py \\'''

# Set kickstart label.
print "  --kickstart-label '%s' \\" % (options.kickstart_label, )

# Set virtualization type to none. This value is not
# obtainable from a kickstart profile via the Satellite API.
print "  --kickstart-virt none \\"

# Get child channels: Systems > Kickstart > Profiles >
# Kickstart Details > Operating System
try:
  tree = client.kickstart.profile.getKickstartTree(
    key,
    options.kickstart_label,
  )
except xmlrpclib.Fault, e:
  print >> sys.stderr, str(e)
  print >> sys.stderr, options
  sys.exit(1)

print "  --kickstart-tree '%s' \\" % (tree, )

# Set Satellite. We use the current Satellite since we have
# no option via the Satellite API.
#u = urlparse.urlparse(options.satellite_url)
print "  --kickstart-satellite $SATELLITE \\"

# Get root password: Systems > Kickstart > Profiles > System
# Details > Details
print "  --kickstart-root redhat \\"

# Get child channels: Systems > Kickstart > Profiles >
# Kickstart Details > Operating System
try:
  child_channels = client.kickstart.profile.getChildChannels(
    key,
    options.kickstart_label,
  )
except xmlrpclib.Fault, e:
  print >> sys.stderr, str(e)
  print >> sys.stderr, options
  sys.exit(1)

print "  --kickstart-childchannels '%s' \\" % (','.join(child_channels))

# Get cfg and rcomm: Systems > Kickstart > Profiles > System
# Details > Details
try:
  cfgmgt = client.kickstart.profile.system.checkConfigManagement(
    key,
    options.kickstart_label,
  )
except xmlrpclib.Fault, e:
  print >> sys.stderr, str(e)
  print >> sys.stderr, options
  sys.exit(1)

if cfgmgt:
  print "  --kickstart-configmgt true \\"

try:
  remotecmds = client.kickstart.profile.system.checkRemoteCommands(
    key,
    options.kickstart_label,
  )
except xmlrpclib.Fault, e:
  print >> sys.stderr, str(e)
  print >> sys.stderr, options
  sys.exit(1)

if remotecmds:
  print "  --kickstart-remotecmds true \\"

# Get partitioning: Systems > Kickstart > Profiles > System
# Details > Partitioning
try:
  partitioning = client.kickstart.profile.system.getPartitioningScheme(
    key,
    options.kickstart_label,
  )
except xmlrpclib.Fault, e:
  print >> sys.stderr, str(e)
  print >> sys.stderr, options
  sys.exit(1)

print "  --kickstart-partitioning '%s' \\" % (','.join(partitioning),)

# Get GPG and SSL keys: Systems > Kickstart > Profiles > System
# Details > GPG & SSL
try:
  keys = client.kickstart.profile.system.listKeys(
    key,
    options.kickstart_label,
  )
except xmlrpclib.Fault, e:
  print >> sys.stderr, str(e)
  print >> sys.stderr, options
  sys.exit(1)

klist = [i['description'] for i in keys]
print "  --kickstart-keys '%s' \\" % (','.join(klist),)

# Get advanced options: Systems > Kickstart > Profiles >
# Kickstart Details > Advanced Options
try:
  advanced_options = client.kickstart.profile.getAdvancedOptions(
    key,
    options.kickstart_label,
  )
except xmlrpclib.Fault, e:
  print >> sys.stderr, str(e)
  print >> sys.stderr, options
  sys.exit(1)

order = ['autostep', 'interactive', 'install', 'upgrade', 'text', 'network', 'cdrom', 'harddrive', 'nfs', 'url', 'lang', 'langsupport', 'keyboard', 'mouse', 'device', 'deviceprobe', 'zerombr', 'clearpart', 'bootloader', 'timezone', 'auth', 'rootpw', 'selinux', 'reboot', 'firewall', 'xconfig', 'skipx', 'key', 'ignoredisk', 'autopart', 'cmdline', 'firstboot', 'graphical', 'iscsi', 'iscsiname', 'logging', 'monitor', 'multipath', 'poweroff', 'halt', 'service', 'shutdown', 'user', 'vnc', 'zfcp']
map = {}
for a in advanced_options:
  try:
    map[a['name']] = a['arguments']
  except KeyError, e:
    map[a['name']] = None

for o in order:
  if map.has_key(o):
    if map[o]:
      if o == 'url':
        dummy = re.sub('org/\d+/', 'org/$ORGNUM/', map[o])
        print "  --kickstart-%s '%s' \\" % (o, dummy)
      elif o == 'rootpw':
        print "  --kickstart-%s '%s' \\" % (o, map[o])
      elif o == 'bootloader':
        print "  --kickstart-%s '%s' \\" % (o, map[o])
      else:
        print "  --kickstart-%s '%s' \\" % (o, map[o])
    else:
      print "  --kickstart-%s true \\" % (o, )

# Get custom options: Systems > Kickstart > Profiles >
# Kickstart Details > Advanced Options > last item (Custom
# options)
try:
  custom_options = client.kickstart.profile.getCustomOptions(
    key,
    options.kickstart_label,
  )
except xmlrpclib.Fault, e:
  print >> sys.stderr, str(e)
  print >> sys.stderr, options
  sys.exit(1)

if custom_options:
  print "  --kickstart-custom \'%s\' \\" % (custom_options[0]['arguments'],)

# Get rpms: Systems > Kickstart > Profiles > Software >
# Package Groups
try:
  rpms = client.kickstart.profile.software.getSoftwareList(
    key,
    options.kickstart_label,
  )
except xmlrpclib.Fault, e:
  print >> sys.stderr, str(e)
  print >> sys.stderr, options
  sys.exit(1)

if rpms:
  print "  --kickstart-software '%s' \\" % (','.join(rpms),)
else:
  print "  --kickstart-software '' \\"

# Get activation key: Systems > Kickstart > Profiles >
# Activation Keys > <activation key>
try:
  akeys = client.kickstart.profile.keys.getActivationKeys(
    key,
    options.kickstart_label,
  )
except xmlrpclib.Fault, e:
  print >> sys.stderr, str(e)
  print >> sys.stderr, options
  sys.exit(1)

if akeys:
  akeys = ['$ORGNUM-%s' % (re.sub('\d+-', '', a['key'], count=1), ) for a in akeys]
  print "  --kickstart-activationkey %s \\" % (','.join(akeys), )
else:
  print "  --kickstart-activationkey '' \\"

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
  sys.exit(1)

if len(scripts) > 2:
  print >> sys.stderr, "Error: only a pre and post script allowed in kickstart convention"
  sys.exit(1)

pre = None
post = None
if scripts:
  for s in scripts:
    c = escape_quote(s['contents'])
    if s['script_type'] == 'pre':
      pre = "  --kickstart-prescript '%s' \\" % (c, )
    else:
      post = "  --kickstart-postscript '%s'" % (c, )
  if pre:
    print pre
  if post:
    print post
  else:
    print "  --kickstart-postscript ''"
else:
  print "  --kickstart-postscript ''"

client.auth.logout(key)
