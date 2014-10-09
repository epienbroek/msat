#!/usr/bin/python

#
# SCRIPT
#   msat_wr_ak.py
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
# HISTORY
# LICENSE
#   Copyright (C) 2013 Allard Berends
#
#   msat_wr_ak.py is free software; you can redistribute it
#   and/or modify it under the terms of the GNU General
#   Public License as published by the Free Software
#   Foundation; either version 3 of the License, or (at your
#   option) any later version.
#
#   msat_wr_ak.py is distributed in the hope that it will be
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
import re
import sys
import time
import xmlrpclib

usage = '''writes specified activation key to stdout'''

description = '''This script writes the creation script of the specified activation key. The '1-' of the organisation must be provided.'''

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
  "--activationkey-label",
  action = "callback",
  callback = config.parse_string,
  dest = "activationkey_label",
  type = "string",
  default = None,
  help = "activationkey label"
)
parser.add_option(
  "-e",
  "--activationkey-existence",
  action = "callback",
  callback = config.parse_boolean,
  dest = "activationkey_existence",
  type = "string",
  default = None,
  help = "test for activationkey existence in regeneration script"
)
parser.add_option(
  "--activationkey-banner",
  action = "callback",
  callback = config.parse_boolean,
  dest = "activationkey_banner",
  type = "string",
  default = 'yes',
  help = "output bash script banner, default is yes"
)
(options, args) = config.get_conf(parser)

if options.satellite_url is None:
  parser.error('Error: specify URL, -u or --satellite-url')
if options.satellite_login is None:
  parser.error('Error: specify login, -l or --login')
if options.satellite_password is None:
  parser.error('Error: specify password, -p or --password')
if options.activationkey_label is None:
  parser.error('specify activationkey label, -l or --activationkey-label. Use list_activation_keys.py to find all activationkey labels.')

# Get session key via auth namespace.
client = xmlrpclib.ServerProxy(options.satellite_url, verbose=0)
key = client.auth.login(options.satellite_login, options.satellite_password)

script = 'ak-' + re.sub('\d+-', '', options.activationkey_label, 1) + '.sh'
t = time.strftime("%Y-%m-%d %H:%M", time.localtime())
y = time.strftime("%Y", time.localtime())
print '#!/bin/bash'

if options.activationkey_banner:
  print '''#
# SCRIPT
#   ''' + script + '''
# DESCRIPTION
#   This script creates the ''' + re.sub('\d+-', '', options.activationkey_label, 1) + '''
#   activation key.
# ARGUMENTS
#   None.
# RETURN
#   0: success.
# DEPENDENCIES
#   This script depends on a functioning Satellite server to
#   connect to.
# FAILURE
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
#'''

ak_label = re.sub('\d+-', '', options.activationkey_label, 1)

if options.activationkey_existence:
  print  '''if [ -n "$(msat_ls_ak.py | /bin/grep '^[0-9]\{1,\}-%s$')" ]; then
  /bin/echo "INFO: %s already exists! Bailing out."
  exit 0
fi
''' % (ak_label, ak_label)

print '''
msat_mk_ak.py \\'''

# Set activationkey label.
print "  --activationkey-label %s \\" % (ak_label, )

# Get description: Systems > Activation Keys > Details
# Get base channels: Systems > Activation Keys > Details
# Get add-on entitlements: Systems > Activation Keys >
# Details
try:
  details = client.activationkey.getDetails(
    key,
    options.activationkey_label,
  )
except xmlrpclib.Fault, e:
  print >> sys.stderr, str(e)
  print >> sys.stderr, options
  sys.exit(1)

print "  --activationkey-description %s \\" % (details['description'], )
if details['base_channel_label'] == 'none':
  print "  --activationkey-basechannel '' \\"
else:
  print "  --activationkey-basechannel %s \\" % (details['base_channel_label'], )
if 'monitoring_entitled' in details['entitlements']:
  print "  --activationkey-monitoring true \\"
else:
  print "  --activationkey-monitoring false \\"
if 'provisioning_entitled' in details['entitlements']:
  print "  --activationkey-provisioning true \\"
else:
  print "  --activationkey-provisioning false \\"
if 'virtualization_host' in details['entitlements']:
  print "  --activationkey-virtualization true \\"
else:
  print "  --activationkey-virtualization false \\"
if 'virtualization_host_platform' in details['entitlements']:
  print "  --activationkey-node true \\"
else:
  print "  --activationkey-node false \\"

# Get configuration file deployment: Systems > Activation
# Keys > Details
try:
  cfgdep = client.activationkey.checkConfigDeployment(
    key,
    options.activationkey_label,
  )
except xmlrpclib.Fault, e:
  print >> sys.stderr, str(e)
  print >> sys.stderr, options
  sys.exit(1)

if cfgdep:
  print "  --activationkey-configuration true \\"

# Get universal default: Systems > Activation Keys > Details
if details['universal_default']:
  print "  --activationkey-universal true \\"
else:
  print "  --activationkey-universal false \\"

# Get child channels: Systems > Activation Keys > Child
# Channels
print "  --activationkey-childchannels '%s' \\" % (','.join(details['child_channel_labels']))

# Get packages: Systems > Activation Keys > Packages
print "  --activationkey-packages '%s' \\" % (','.join([p['name'] for p in details['packages']]))

# Get config channels: Systems > Activation Keys >
# Configuration > List/Unsubscribe from Channels
try:
  cfgchannels = client.activationkey.listConfigChannels(
    key,
    options.activationkey_label,
  )
except xmlrpclib.Fault, e:
  print "  --activationkey-configchannels ''"
  #print >> sys.stderr, str(e)
  #print >> sys.stderr, options
else:
  print "  --activationkey-configchannels '%s'" % (','.join([c['label'] for c in cfgchannels]), )

client.auth.logout(key)
