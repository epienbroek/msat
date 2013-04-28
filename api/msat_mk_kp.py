#!/usr/bin/python

#
# SCRIPT
#   msat_mk_kp.py
# DESCRIPTION
#   Add a software channel via the command line. See the
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
#   If you put single quotes around value, but forget to
#   escape embedded single quotes, this script will fail.
#   Escaping works like this:
#   $ echo 'don'"'"'t'
#   don't
#   So ' -> '"'"'
#   Complicated huh?
# AUTHORS
#   Date strings made with 'date +"\%Y-\%m-\%d \%H:\%M"'.
#   Allard Berends (AB),  2013-02-24 13:07
# HISTORY
#   2013-02-24 13:07, AB: added optionsiguration files option.
# LICENSE
#   Copyright (C) 2013 Allard Berends
# 
#   msat_mk_kp.py is free software; you can redistribute it
#   and/or modify it under the terms of the GNU General
#   Public License as published by the Free Software
#   Foundation; either version 3 of the License, or (at your
#   option) any later version.
#
#   msat_mk_kp.py is distributed in the hope that it will be
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

usage = '''adds the specified kickstart profile to the specified kickstartable tree'''

description = '''This script adds the specified kickstart profile to the specified kickstartable tree. If the kickstartable tree does not exist, an error will be given and a dump of the used parameters. If the kickstart profile already exists, an error will be given and a dump of the used parameters. The kickstart profile must be removed first before this script succeeds.'''

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
  "--kickstart-label",
  action = "callback",
  callback = config.parse_string,
  dest = "kickstart_label",
  type = "string",
  default = None,
  help = "label kickstart option"
)
parser.add_option(
  "--kickstart-virt",
  action = "callback",
  callback = config.parse_string,
  dest = "kickstart_virt",
  type = "string",
  default = None,
  help = "virt kickstart option"
)
parser.add_option(
  "--kickstart-tree",
  action = "callback",
  callback = config.parse_string,
  dest = "kickstart_tree",
  type = "string",
  default = None,
  help = "tree kickstart option"
)
parser.add_option(
  "--kickstart-satellite",
  action = "callback",
  callback = config.parse_string,
  dest = "kickstart_satellite",
  type = "string",
  default = None,
  help = "satellite kickstart option"
)
parser.add_option(
  "--kickstart-root",
  action = "callback",
  callback = config.parse_string,
  dest = "kickstart_root",
  type = "string",
  default = None,
  help = "root kickstart option"
)
parser.add_option(
  "--kickstart-childchannels",
  action = "callback",
  callback = config.parse_string,
  dest = "kickstart_childchannels",
  type = "string",
  default = None,
  help = "childchannels kickstart option"
)
parser.add_option(
  "--kickstart-activationkey",
  action = "callback",
  callback = config.parse_string,
  dest = "kickstart_activationkey",
  type = "string",
  default = None,
  help = "activationkey kickstart option"
)
parser.add_option(
  "--kickstart-configmgt",
  action = "callback",
  callback = config.parse_boolean,
  dest = "kickstart_configmgt",
  type = "string",
  default = True,
  help = "configmgt kickstart option"
)
parser.add_option(
  "--kickstart-remotecmds",
  action = "callback",
  callback = config.parse_boolean,
  dest = "kickstart_remotecmds",
  type = "string",
  default = True,
  help = "remotecmds kickstart option"
)
parser.add_option(
  "--kickstart-partitioning",
  action = "callback",
  callback = config.parse_string,
  dest = "kickstart_partitioning",
  type = "string",
  default = None,
  help = "partitioning kickstart option"
)
parser.add_option(
  "--kickstart-keys",
  action = "callback",
  callback = config.parse_string,
  dest = "kickstart_keys",
  type = "string",
  default = None,
  help = "keys kickstart option"
)
parser.add_option(
  "--kickstart-software",
  action = "callback",
  callback = config.parse_string,
  dest = "kickstart_software",
  type = "string",
  default = None,
  help = "software kickstart option"
)
parser.add_option(
  "--kickstart-script",
  action = "callback",
  callback = config.parse_file,
  dest = "kickstart_script",
  type = "string",
  default = None,
  help = "script kickstart option"
)
parser.add_option(
  "--kickstart-autostep",
  action   = "callback",
  callback = config.parse_string,
  dest     = "kickstart_autostep",
  type     = "string",
  default  = "",
  help     = "autostep kickstart advanced option"
)
parser.add_option(
  "--kickstart-interactive",
  action   = "callback",
  callback = config.parse_string,
  dest     = "kickstart_interactive",
  type     = "string",
  default  = "",
  help     = "interactive kickstart advanced option"
)
parser.add_option(
  "--kickstart-install",
  action   = "callback",
  callback = config.parse_string,
  dest     = "kickstart_install",
  type     = "string",
  default  = "true",
  help     = "install kickstart advanced option"
)
parser.add_option(
  "--kickstart-upgrade",
  action   = "callback",
  callback = config.parse_string,
  dest     = "kickstart_upgrade",
  type     = "string",
  default  = "",
  help     = "upgrade kickstart advanced option"
)
parser.add_option(
  "--kickstart-text",
  action   = "callback",
  callback = config.parse_string,
  dest     = "kickstart_text",
  type     = "string",
  default  = "true",
  help     = "text kickstart advanced option"
)
parser.add_option(
  "--kickstart-network",
  action   = "callback",
  callback = config.parse_string,
  dest     = "kickstart_network",
  type     = "string",
  default  = None,
  help     = "network kickstart advanced option"
)
parser.add_option(
  "--kickstart-cdrom",
  action   = "callback",
  callback = config.parse_string,
  dest     = "kickstart_cdrom",
  type     = "string",
  default  = "",
  help     = "cdrom kickstart advanced option"
)
parser.add_option(
  "--kickstart-harddrive",
  action   = "callback",
  callback = config.parse_string,
  dest     = "kickstart_harddrive",
  type     = "string",
  default  = "",
  help     = "harddrive kickstart advanced option"
)
parser.add_option(
  "--kickstart-nfs",
  action   = "callback",
  callback = config.parse_string,
  dest     = "kickstart_nfs",
  type     = "string",
  default  = "",
  help     = "nfs kickstart advanced option"
)
parser.add_option(
  "--kickstart-url",
  action   = "callback",
  callback = config.parse_string,
  dest     = "kickstart_url",
  type     = "string",
  default  = None,
  help     = "url kickstart advanced option"
)
parser.add_option(
  "--kickstart-lang",
  action   = "callback",
  callback = config.parse_string,
  dest     = "kickstart_lang",
  type     = "string",
  default  = None,
  help     = "lang kickstart advanced option"
)
parser.add_option(
  "--kickstart-langsupport",
  action   = "callback",
  callback = config.parse_string,
  dest     = "kickstart_langsupport",
  type     = "string",
  default  = None,
  help     = "langsupport kickstart advanced option"
)
parser.add_option(
  "--kickstart-keyboard",
  action   = "callback",
  callback = config.parse_string,
  dest     = "kickstart_keyboard",
  type     = "string",
  default  = None,
  help     = "keyboard kickstart advanced option"
)
parser.add_option(
  "--kickstart-mouse",
  action   = "callback",
  callback = config.parse_string,
  dest     = "kickstart_mouse",
  type     = "string",
  default  = None,
  help     = "mouse kickstart advanced option"
)
parser.add_option(
  "--kickstart-device",
  action   = "callback",
  callback = config.parse_string,
  dest     = "kickstart_device",
  type     = "string",
  default  = None,
  help     = "device kickstart advanced option"
)
parser.add_option(
  "--kickstart-deviceprobe",
  action   = "callback",
  callback = config.parse_string,
  dest     = "kickstart_deviceprobe",
  type     = "string",
  default  = None,
  help     = "deviceprobe kickstart advanced option"
)
parser.add_option(
  "--kickstart-zerombr",
  action   = "callback",
  callback = config.parse_string,
  dest     = "kickstart_zerombr",
  type     = "string",
  default  = None,
  help     = "zerombr kickstart advanced option"
)
parser.add_option(
  "--kickstart-clearpart",
  action   = "callback",
  callback = config.parse_string,
  dest     = "kickstart_clearpart",
  type     = "string",
  default  = None,
  help     = "clearpart kickstart advanced option"
)
parser.add_option(
  "--kickstart-bootloader",
  action   = "callback",
  callback = config.parse_string,
  dest     = "kickstart_bootloader",
  type     = "string",
  default  = None,
  help     = "bootloader kickstart advanced option"
)
parser.add_option(
  "--kickstart-timezone",
  action   = "callback",
  callback = config.parse_string,
  dest     = "kickstart_timezone",
  type     = "string",
  default  = None,
  help     = "timezone kickstart advanced option"
)
parser.add_option(
  "--kickstart-auth",
  action   = "callback",
  callback = config.parse_string,
  dest     = "kickstart_auth",
  type     = "string",
  default  = None,
  help     = "auth kickstart advanced option"
)
parser.add_option(
  "--kickstart-rootpw",
  action   = "callback",
  callback = config.parse_string,
  dest     = "kickstart_rootpw",
  type     = "string",
  default  = None,
  help     = "rootpw kickstart advanced option"
)
parser.add_option(
  "--kickstart-selinux",
  action   = "callback",
  callback = config.parse_string,
  dest     = "kickstart_selinux",
  type     = "string",
  default  = None,
  help     = "selinux kickstart advanced option"
)
parser.add_option(
  "--kickstart-reboot",
  action   = "callback",
  callback = config.parse_string,
  dest     = "kickstart_reboot",
  type     = "string",
  default  = "true",
  help     = "reboot kickstart advanced option"
)
parser.add_option(
  "--kickstart-firewall",
  action   = "callback",
  callback = config.parse_string,
  dest     = "kickstart_firewall",
  type     = "string",
  default  = None,
  help     = "firewall kickstart advanced option"
)
parser.add_option(
  "--kickstart-xconfig",
  action   = "callback",
  callback = config.parse_string,
  dest     = "kickstart_xconfig",
  type     = "string",
  default  = None,
  help     = "xconfig kickstart advanced option"
)
parser.add_option(
  "--kickstart-skipx",
  action   = "callback",
  callback = config.parse_string,
  dest     = "kickstart_skipx",
  type     = "string",
  default  = "true",
  help     = "skipx kickstart advanced option"
)
parser.add_option(
  "--kickstart-key",
  action   = "callback",
  callback = config.parse_string,
  dest     = "kickstart_key",
  type     = "string",
  default  = "--skip",
  help     = "key kickstart advanced option"
)
parser.add_option(
  "--kickstart-ignoredisk",
  action   = "callback",
  callback = config.parse_string,
  dest     = "kickstart_ignoredisk",
  type     = "string",
  default  = None,
  help     = "ignoredisk kickstart advanced option"
)
parser.add_option(
  "--kickstart-autopart",
  action   = "callback",
  callback = config.parse_string,
  dest     = "kickstart_autopart",
  type     = "string",
  default  = "",
  help     = "autopart kickstart advanced option"
)
parser.add_option(
  "--kickstart-cmdline",
  action   = "callback",
  callback = config.parse_string,
  dest     = "kickstart_cmdline",
  type     = "string",
  default  = "",
  help     = "cmdline kickstart advanced option"
)
parser.add_option(
  "--kickstart-firstboot",
  action   = "callback",
  callback = config.parse_string,
  dest     = "kickstart_firstboot",
  type     = "string",
  default  = None,
  help     = "firstboot kickstart advanced option"
)
parser.add_option(
  "--kickstart-graphical",
  action   = "callback",
  callback = config.parse_string,
  dest     = "kickstart_graphical",
  type     = "string",
  default  = "",
  help     = "graphical kickstart advanced option"
)
parser.add_option(
  "--kickstart-iscsi",
  action   = "callback",
  callback = config.parse_string,
  dest     = "kickstart_iscsi",
  type     = "string",
  default  = None,
  help     = "iscsi kickstart advanced option"
)
parser.add_option(
  "--kickstart-iscsiname",
  action   = "callback",
  callback = config.parse_string,
  dest     = "kickstart_iscsiname",
  type     = "string",
  default  = None,
  help     = "iscsiname kickstart advanced option"
)
parser.add_option(
  "--kickstart-logging",
  action   = "callback",
  callback = config.parse_string,
  dest     = "kickstart_logging",
  type     = "string",
  default  = None,
  help     = "logging kickstart advanced option"
)
parser.add_option(
  "--kickstart-monitor",
  action   = "callback",
  callback = config.parse_string,
  dest     = "kickstart_monitor",
  type     = "string",
  default  = None,
  help     = "monitor kickstart advanced option"
)
parser.add_option(
  "--kickstart-multipath",
  action   = "callback",
  callback = config.parse_string,
  dest     = "kickstart_multipath",
  type     = "string",
  default  = None,
  help     = "multipath kickstart advanced option"
)
parser.add_option(
  "--kickstart-poweroff",
  action   = "callback",
  callback = config.parse_string,
  dest     = "kickstart_poweroff",
  type     = "string",
  default  = "",
  help     = "poweroff kickstart advanced option"
)
parser.add_option(
  "--kickstart-halt",
  action   = "callback",
  callback = config.parse_string,
  dest     = "kickstart_halt",
  type     = "string",
  default  = "",
  help     = "halt kickstart advanced option"
)
parser.add_option(
  "--kickstart-services",
  action   = "callback",
  callback = config.parse_string,
  dest     = "kickstart_services",
  type     = "string",
  default  = None,
  help     = "services kickstart advanced option"
)
parser.add_option(
  "--kickstart-shutdown",
  action   = "callback",
  callback = config.parse_string,
  dest     = "kickstart_shutdown",
  type     = "string",
  default  = "",
  help     = "shutdown kickstart advanced option"
)
parser.add_option(
  "--kickstart-user",
  action   = "callback",
  callback = config.parse_string,
  dest     = "kickstart_user",
  type     = "string",
  default  = None,
  help     = "user kickstart advanced option"
)
parser.add_option(
  "--kickstart-vnc",
  action   = "callback",
  callback = config.parse_string,
  dest     = "kickstart_vnc",
  type     = "string",
  default  = None,
  help     = "vnc kickstart advanced option"
)
parser.add_option(
  "--kickstart-zfcp",
  action   = "callback",
  callback = config.parse_string,
  dest     = "kickstart_zfcp",
  type     = "string",
  default  = None,
  help     = "zfcp kickstart advanced option"
)

(options, args) = config.get_conf(parser)

if options.satellite_url is None:
  parser.error('Error: specify URL, -u or --satellite-url')
if options.satellite_login is None:
  parser.error('Error: specify login, -l or --login')
if options.satellite_password is None:
  parser.error('Error: specify password, -p or --password')
if options.kickstart_label is None:
  parser.error('Error: specify label, -l or --kickstart-label')
if not options.kickstart_virt in ['none', 'para_host', 'qemu', 'xenfv', 'xenpv']:
  parser.error('Error: specify virt, -v or --kickstart-virt must be one of none, para_host, qemu, xenfv, xenpv')
if options.kickstart_tree is None:
  parser.error('Error: specify tree, -t or --kickstart-tree')
if options.kickstart_satellite is None:
  parser.error('Error: specify satellite, -s or --kickstart-satellite')
if options.kickstart_root is None:
  parser.error('Error: specify root, -r or --kickstart-root')
#print options
#sys.exit(1)
advanced_options = []
if options.kickstart_autostep:
  advanced_options.append({'name':      'autostep',
                           'arguments': options.kickstart_autostep})

if options.kickstart_interactive:
  advanced_options.append({'name':      'interactive',
                           'arguments': options.kickstart_interactive})

if options.kickstart_install:
  advanced_options.append({'name':      'install',
                           'arguments': options.kickstart_install})

if options.kickstart_upgrade:
  advanced_options.append({'name':      'upgrade',
                           'arguments': options.kickstart_upgrade})

if options.kickstart_text:
  advanced_options.append({'name':      'text',
                           'arguments': options.kickstart_text})

if options.kickstart_network:
  advanced_options.append({'name':      'network',
                           'arguments': options.kickstart_network})

if options.kickstart_cdrom:
  advanced_options.append({'name':      'cdrom',
                           'arguments': options.kickstart_cdrom})

if options.kickstart_harddrive:
  advanced_options.append({'name':      'harddrive',
                           'arguments': options.kickstart_harddrive})

if options.kickstart_nfs:
  advanced_options.append({'name':      'nfs',
                           'arguments': options.kickstart_nfs})

if options.kickstart_url:
  advanced_options.append({'name':      'url',
                           'arguments': options.kickstart_url})

if not options.kickstart_lang:
  print >> sys.stderr, "option --lang is required"
  sys.exit(1)
else:
  advanced_options.append({'name':      'lang',
                           'arguments': options.kickstart_lang})

if options.kickstart_langsupport:
  advanced_options.append({'name':      'langsupport',
                           'arguments': options.kickstart_langsupport})

if not options.kickstart_keyboard:
  print >> sys.stderr, "option --keyboard is required"
  sys.exit(1)
else:
  advanced_options.append({'name':      'keyboard',
                           'arguments': options.kickstart_keyboard})

if options.kickstart_mouse:
  advanced_options.append({'name':      'mouse',
                           'arguments': options.kickstart_mouse})

if options.kickstart_device:
  # AB: hack to keep < 5.5 in line with 5.5.
  if options.satellite_version in ['5.3', '5.4'] and options.kickstart_device == 'cciss':
    options.kickstart_device = 'scsi cciss'
  advanced_options.append({'name':      'device',
                           'arguments': options.kickstart_device})

if options.kickstart_deviceprobe:
  advanced_options.append({'name':      'deviceprobe',
                           'arguments': options.kickstart_deviceprobe})

if options.kickstart_zerombr:
  advanced_options.append({'name':      'zerombr',
                           'arguments': options.kickstart_zerombr})

if options.kickstart_clearpart:
  advanced_options.append({'name':      'clearpart',
                           'arguments': options.kickstart_clearpart})

if not options.kickstart_bootloader:
  print >> sys.stderr, "option --bootloader is required"
  sys.exit(1)
else:
  advanced_options.append({'name':      'bootloader',
                           'arguments': options.kickstart_bootloader})

if not options.kickstart_timezone:
  print >> sys.stderr, "option --timezone is required"
  sys.exit(1)
else:
  advanced_options.append({'name':      'timezone',
                           'arguments': options.kickstart_timezone})

if not options.kickstart_auth:
  print >> sys.stderr, "option --auth is required"
  sys.exit(1)
else:
  advanced_options.append({'name':      'auth',
                           'arguments': options.kickstart_auth})

if not options.kickstart_rootpw:
  print >> sys.stderr, "option --rootpw is required"
  sys.exit(1)
else:
  advanced_options.append({'name':      'rootpw',
                           'arguments': options.kickstart_rootpw})

if options.kickstart_selinux:
  advanced_options.append({'name':      'selinux',
                           'arguments': options.kickstart_selinux})

if options.kickstart_reboot:
  advanced_options.append({'name':      'reboot',
                           'arguments': options.kickstart_reboot})

if options.kickstart_firewall:
  advanced_options.append({'name':      'firewall',
                           'arguments': options.kickstart_firewall})

if options.kickstart_xconfig:
  advanced_options.append({'name':      'xoptionsig',
                           'arguments': options.kickstart_xoptionsig})

if options.kickstart_skipx:
  advanced_options.append({'name':      'skipx',
                           'arguments': options.kickstart_skipx})

if options.kickstart_key:
  advanced_options.append({'name':      'key',
                           'arguments': options.kickstart_key})

if options.kickstart_ignoredisk:
  advanced_options.append({'name':      'ignoredisk',
                           'arguments': options.kickstart_ignoredisk})

if options.kickstart_autopart:
  advanced_options.append({'name':      'autopart',
                           'arguments': options.kickstart_autopart})

if options.kickstart_cmdline:
  advanced_options.append({'name':      'cmdline',
                           'arguments': options.kickstart_cmdline})

if options.kickstart_firstboot:
  advanced_options.append({'name':      'firstboot',
                           'arguments': options.kickstart_firstboot})

if options.kickstart_graphical:
  advanced_options.append({'name':      'graphical',
                           'arguments': options.kickstart_graphical})

if options.kickstart_iscsi:
  advanced_options.append({'name':      'iscsi',
                           'arguments': options.kickstart_iscsi})

if options.kickstart_iscsiname:
  advanced_options.append({'name':      'iscsiname',
                           'arguments': options.kickstart_iscsiname})

if options.kickstart_logging:
  advanced_options.append({'name':      'logging',
                           'arguments': options.kickstart_logging})

if options.kickstart_monitor:
  advanced_options.append({'name':      'monitor',
                           'arguments': options.kickstart_monitor})

if options.kickstart_multipath:
  advanced_options.append({'name':      'multipath',
                           'arguments': options.kickstart_multipath})

if options.kickstart_poweroff:
  advanced_options.append({'name':      'poweroff',
                           'arguments': options.kickstart_poweroff})

if options.kickstart_halt:
  advanced_options.append({'name':      'halt',
                           'arguments': options.kickstart_halt})

if options.kickstart_services:
  advanced_options.append({'name':      'services',
                           'arguments': options.kickstart_services})

if options.kickstart_shutdown:
  advanced_options.append({'name':      'shutdown',
                           'arguments': options.kickstart_shutdown})

if options.kickstart_user:
  advanced_options.append({'name':      'user',
                           'arguments': options.kickstart_user})

if options.kickstart_vnc:
  advanced_options.append({'name':      'vnc',
                           'arguments': options.kickstart_vnc})

if options.kickstart_zfcp:
  advanced_options.append({'name':      'zfcp',
                           'arguments': options.kickstart_zfcp})

if options.kickstart_childchannels:
  child_channels = options.kickstart_childchannels.split(',')

if options.kickstart_partitioning:
  partitioning = options.kickstart_partitioning.split(',')

if options.kickstart_keys:
  keys = options.kickstart_keys.split(',')

if options.kickstart_software:
  software_list = options.kickstart_software.split(',')

if options.kickstart_activationkey:
  activationkey_list = options.kickstart_activationkey.split(',')

# Get session key via auth namespace.
client = xmlrpclib.ServerProxy(options.satellite_url, verbose=0)
key = client.auth.login(options.satellite_login, options.satellite_password)

# create kickstart profile
try:
  rc = client.kickstart.createProfile(
    key,
    options.kickstart_label,
    options.kickstart_virt,
    options.kickstart_tree,
    options.kickstart_satellite,
    options.kickstart_root,
  )
except xmlrpclib.Fault, e:
  print >> sys.stderr, str(e)
  print >> sys.stderr, options
  sys.exit(1)

if options.satellite_version == '5.5':
  try:
    rc = client.kickstart.profile.setCfgPreservation(
      key,
      options.kickstart_label,
      True,
    )
  except xmlrpclib.Fault, e:
    print >> sys.stderr, str(e)
    print >> sys.stderr, options
    sys.exit(1)

if options.satellite_version == '5.5':
  try:
    rc = client.kickstart.profile.setLogging(
      key,
      options.kickstart_label,
      True,
      True,
    )
  except xmlrpclib.Fault, e:
    print >> sys.stderr, str(e)
    print >> sys.stderr, options
    sys.exit(1)

if advanced_options:
  try:
    rc = client.kickstart.profile.setAdvancedOptions(
      key,
      options.kickstart_label,
      advanced_options
    )
  except xmlrpclib.Fault, e:
    print >> sys.stderr, str(e)
    print >> sys.stderr, options

try:
  if child_channels:
    try:
      rc = client.kickstart.profile.setChildChannels(
        key,
        options.kickstart_label,
        child_channels
      )
    except xmlrpclib.Fault, e:
      print >> sys.stderr, str(e)
      print >> sys.stderr, options
except NameError, e:
  pass

try:
  if activationkey_list:
    try:
      for activationkey in activationkey_list:
        rc = client.kickstart.profile.keys.addActivationKey(
          key,
          options.kickstart_label,
          activationkey
        )
    except xmlrpclib.Fault, e:
      print >> sys.stderr, str(e)
      print >> sys.stderr, options
except NameError, e:
  pass

if options.kickstart_configmgt:
  try:
    rc = client.kickstart.profile.system.enableConfigManagement(
      key,
      options.kickstart_label,
    )
  except xmlrpclib.Fault, e:
    print >> sys.stderr, str(e)
    print >> sys.stderr, options

if options.kickstart_partitioning:
  try:
    rc = client.kickstart.profile.system.setPartitioningScheme(
      key,
      options.kickstart_label,
      partitioning
    )
  except xmlrpclib.Fault, e:
    print >> sys.stderr, str(e)
    print >> sys.stderr, options

if options.kickstart_keys:
  try:
    rc = client.kickstart.profile.system.addKeys(
      key,
      options.kickstart_label,
      keys
    )
  except xmlrpclib.Fault, e:
    print >> sys.stderr, str(e)
    print >> sys.stderr, options

if options.kickstart_software:
  try:
    rc = client.kickstart.profile.software.setSoftwareList(
      key,
      options.kickstart_label,
      software_list
    )
  except xmlrpclib.Fault, e:
    print >> sys.stderr, str(e)
    print >> sys.stderr, options

if options.satellite_version == '5.5':
  if options.kickstart_script:
    try:
      rc = client.kickstart.profile.addScript(
        key,
        options.kickstart_label,
        options.kickstart_script,
        '',
        'post',
        True,
        True
      )
    except xmlrpclib.Fault, e:
      print >> sys.stderr, str(e)
      print >> sys.stderr, options
else:
  if options.kickstart_script:
    try:
      rc = client.kickstart.profile.addScript(
        key,
        options.kickstart_label,
        options.kickstart_script,
        '',
        'post',
        True
      )
    except xmlrpclib.Fault, e:
      print >> sys.stderr, str(e)
      print >> sys.stderr, options

# Due to bug 679846 we run this one always to force the
# client.kickstart.profile.addScript to function!
try:
  rc = client.kickstart.profile.system.enableRemoteCommands(
    key,
    options.kickstart_label,
  )
except xmlrpclib.Fault, e:
  print >> sys.stderr, str(e)
  print >> sys.stderr, options
if not options.kickstart_remotecmds:
  try:
    rc = client.kickstart.profile.system.disableRemoteCommands(
      key,
      options.kickstart_label,
    )
  except xmlrpclib.Fault, e:
    print >> sys.stderr, str(e)
    print >> sys.stderr, options
client.auth.logout(key)
