#!/usr/bin/python

#
# SCRIPT
#   msat_mk_ak.py
# DESCRIPTION
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
#   msat_mk_ak.py is free software; you can redistribute it
#   and/or modify it under the terms of the GNU General
#   Public License as published by the Free Software
#   Foundation; either version 3 of the License, or (at your
#   option) any later version.
#
#   msat_mk_ak.py is distributed in the hope that it will be
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

usage = '''creates specified activation key'''

description = '''This script creates the specified activation key. The '1-' of the organisation must not be provided. Child channels and config channels can be specified. Furthermore, the list of RPM's to add are specified too.'''

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
  "-l",
  "--activationkey-label",
  action = "callback",
  callback = config.parse_string,
  dest = "activationkey_label",
  type = "string",
  default = None,
  help = "label activationkey option"
)
parser.add_option(
  "--activationkey-description",
  action = "callback",
  callback = config.parse_string,
  dest = "activationkey_description",
  type = "string",
  default = None,
  help = "description activationkey option"
)
parser.add_option(
  "--activationkey-basechannel",
  action = "callback",
  callback = config.parse_string,
  dest = "activationkey_basechannel",
  type = "string",
  default = None,
  help = "basechannel activationkey option"
)
parser.add_option(
  "--activationkey-monitoring",
  action = "callback",
  callback = config.parse_boolean,
  dest = "activationkey_monitoring",
  type = "string",
  default = None,
  help = "monitoring activationkey option"
)
parser.add_option(
  "--activationkey-provisioning",
  action = "callback",
  callback = config.parse_boolean,
  dest = "activationkey_provisioning",
  type = "string",
  default = None,
  help = "provisioning activationkey option"
)
parser.add_option(
  "--activationkey-virtualization",
  action = "callback",
  callback = config.parse_boolean,
  dest = "activationkey_virtualization",
  type = "string",
  default = None,
  help = "virtualization activationkey option"
)
parser.add_option(
  "--activationkey-node",
  action = "callback",
  callback = config.parse_boolean,
  dest = "activationkey_node",
  type = "string",
  default = None,
  help = "node activationkey option"
)
parser.add_option(
  "--activationkey-configuration",
  action = "callback",
  callback = config.parse_boolean,
  dest = "activationkey_configuration",
  type = "string",
  default = None,
  help = "configuration activationkey option"
)
parser.add_option(
  "--activationkey-universal",
  action = "callback",
  callback = config.parse_boolean,
  dest = "activationkey_universal",
  type = "string",
  default = False,
  help = "universal activationkey option"
)
parser.add_option(
  "--activationkey-childchannels",
  action = "callback",
  callback = config.parse_string,
  dest = "activationkey_childchannels",
  type = "string",
  default = None,
  help = "childchannels activationkey option"
)
parser.add_option(
  "--activationkey-packages",
  action = "callback",
  callback = config.parse_string,
  dest = "activationkey_packages",
  type = "string",
  default = None,
  help = "packages activationkey option"
)
parser.add_option(
  "--activationkey-configchannels",
  action = "callback",
  callback = config.parse_string,
  dest = "activationkey_configchannels",
  type = "string",
  default = None,
  help = "configchannels activationkey option"
)

(options, args) = config.get_conf(parser)

if options.satellite_url is None:
  parser.error('Error: specify URL, -u or --satellite-url')
if options.satellite_login is None:
  parser.error('Error: specify login, -l or --login')
if options.satellite_password is None:
  parser.error('Error: specify password, -p or --password')
if options.activationkey_label is None:
  parser.error('Error: specify label, --activationkey-label')
if options.activationkey_description is None:
  parser.error('Error: specify description, --activationkey-description')
if options.activationkey_basechannel is None:
  parser.error('Error: specify basechannel, --basechannel')

addons = []
if options.activationkey_monitoring:
  addons.append('monitoring_entitled')
if options.activationkey_provisioning:
  addons.append('provisioning_entitled')
if options.activationkey_virtualization:
  addons.append('virtualization_host')
if options.activationkey_node:
  addons.append('virtualization_host_platform')

# Get session key via auth namespace.
client = xmlrpclib.ServerProxy(options.satellite_url, verbose=0)
key = client.auth.login(options.satellite_login, options.satellite_password)


try:
  akey = client.activationkey.getDetails(
    key,
    '1-' + options.activationkey_label,
  )
except xmlrpclib.Fault, e:
  pass
else:
  print >> sys.stderr, "%s already exists, skipping" % (options.activationkey_label, )
  sys.exit(1)

try:
  akey = client.activationkey.create(
    key,
    options.activationkey_label,
    options.activationkey_description,
    options.activationkey_basechannel,
    addons,
    options.activationkey_universal
  )
except xmlrpclib.Fault, e:
  print >> sys.stderr, str(e)
  print >> sys.stderr, options
  sys.exit(1)

if options.activationkey_configuration:
  try:
    rc = client.activationkey.enableConfigDeployment(
      key,
      akey
    )
  except xmlrpclib.Fault, e:
    print >> sys.stderr, str(e)
    print >> sys.stderr, options
    sys.exit(1)

if options.activationkey_childchannels:
  childchannels = options.activationkey_childchannels.split(',')
  try:
    rc = client.activationkey.addChildChannels(
      key,
      akey,
      childchannels
    )
  except xmlrpclib.Fault, e:
    print >> sys.stderr, "ERROR in child channels specification"
    print >> sys.stderr, str(e)
    print >> sys.stderr, options
    sys.exit(1)

if options.activationkey_packages:
  packages = options.activationkey_packages.split(',')
  try:
    rc = client.activationkey.addPackageNames(
      key,
      akey,
      packages
    )
  except xmlrpclib.Fault, e:
    print >> sys.stderr, "ERROR in packages specification"
    print >> sys.stderr, str(e)
    print >> sys.stderr, options
    sys.exit(1)

if options.activationkey_configchannels:
  configchannels = options.activationkey_configchannels.split(',')
  try:
    rc = client.activationkey.addConfigChannels(
      key,
      [akey],
      configchannels,
      False
    )
  except xmlrpclib.Fault, e:
    print >> sys.stderr, "ERROR in config channel specification"
    print >> sys.stderr, str(e)
    print >> sys.stderr, options
    sys.exit(1)

client.auth.logout(key)
