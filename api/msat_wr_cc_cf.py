#!/usr/bin/python

#
# SCRIPT
#   msat_wr_cc_cf.py
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
#   Gerben Welter (GW),  2013-04-28 22:41
# HISTORY
#   2013-04-28 22:41, GW added SELinux context support.
# LICENSE
#   Copyright (C) 2013 Allard Berends
#
#   msat_wr_cc_cf.py is free software; you can redistribute
#   it and/or modify it under the terms of the GNU General
#   Public License as published by the Free Software
#   Foundation; either version 3 of the License, or (at your
#   option) any later version.
#
#   msat_wr_cc_cf.py is distributed in the hope that it will
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
import re
import shutil
import stat
import sys
import time
import urlparse
import xmlrpclib

def escape_quote(s):
  # Remove nasty long dash u'u2013' with --
  s = re.sub(u'(?ms)[\u2013\u00ad]', '--', s)
  s = s.encode('ascii')
  # We use here documents, so no ' escaping
  #e = re.sub('(?ms)\'', '\'"\'"\'', s)
  #s = re.sub('(?ms)`', '\`', s)
  #s = re.sub('(?ms)\$', '\\$', s)
  return s

usage = '''writes recreation script of config channel and specified config file(s) to dir'''

description = '''This script writes the specified config file from the specified config channel to a directory named after the config channel or the specified directory name.'''

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
  help = "configchannel label"
)
parser.add_option(
  "-n",
  "--configpath-path",
  action = "callback",
  callback = config.parse_string,
  dest = "configpath_path",
  type = "string",
  default = None,
  help = "path of file or dir, or comma separated list of files or dirs"
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

if options.configchannel_label is None:
  parser.error('Error: specify label, -l or --configchannel-label')
if options.configpath_path is None:
  parser.error('Error: specify path, -n or --configpath-path')
paths = options.configpath_path.split(',')

if options.save_path:
  save_path = os.path.abspath(options.save_path)
else:
  save_path = os.path.abspath(options.configchannel_label)

if os.path.exists(save_path):
  shutil.rmtree(save_path)
os.mkdir(save_path)

# Get session key via auth namespace.
client = xmlrpclib.ServerProxy(options.satellite_url, verbose=0)
key = client.auth.login(options.satellite_login, options.satellite_password)

try:
  files = client.configchannel.lookupFileInfo(
    key,
    options.configchannel_label,
    paths
  )
except xmlrpclib.Fault, e:
  print >> sys.stderr, str(e)
  print >> sys.stderr, options

for f in files:
  script = 'cf-' + re.sub('/', '_', f['path']) + '.sh'
  script_path = os.path.join(save_path, script)
  fd = open(script_path, 'w')
  os.chmod(script_path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
  t = time.strftime("%Y-%m-%d %H:%M", time.localtime())
  y = time.strftime("%Y", time.localtime())
  fd.write('''#!/bin/bash
#
# SCRIPT
#   ''' + script + '''
# DESCRIPTION
#   This script creates the ''' + f['path'] + '''
#   config file.
# ARGUMENTS
#   None.
# RETURN
#   0: success.
# DEPENDENCIES
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
#

msat_mk_cc_cf.py \\
''')

  # Set configchannel label.
  print >> fd, "  --configchannel-label %s \\" % (options.configchannel_label, )
  print >> fd, "  --configpath-path %s \\" % (f['path'], )

  if f['type'] == 'file':
    print >> fd, "  --configpath-dir false \\"
    print >> fd, "  --configpath-content - \\"
  elif f['type'] == 'directory':
    print >> fd, "  --configpath-dir true \\"
  else:
    pass

  if f['type'] == 'file' or f['type'] == 'directory':
    print >> fd, "  --configpath-user %s \\" % (f['owner'], )
    print >> fd, "  --configpath-group %s \\" % (f['group'], )

  try:
    print >> fd, "  --configpath-context '%s' \\" % (f['selinux_ctx'], )
  except KeyError, e:
    # AB: we use pass here since we don't want to clutter up
    # peoples code with empty SELinux contexts when they
    # might not be using SELinux at all.
    #print >> fd, "  --configpath-context '' \\"
    pass
  if f['type'] == 'file':
    print >> fd, "  --configpath-permissions %s \\" % (f['permissions_mode'], )
  elif f['type'] == 'directory':
    print >> fd, "  --configpath-permissions %s" % (f['permissions_mode'], )
  else:
    print >> fd, "  --configpath-link %s" % (f['target_path'], )

  if f['type'] == 'file':
    print >> fd, "  --configpath-startdelimiter '%s' \\" % (f['macro-start-delimiter'], )
    print >> fd, "  --configpath-enddelimiter '%s' << 'EOF__BLAH__EOF'" % (f['macro-end-delimiter'], )
    if f['binary']:
      print >> sys.stderr, "ERROR: %s: %s: binary config files not supported" % (options.configchannel_label, f['path'])
      content = xmlrpclib.Binary.decode(f['contents'])
      print >> fd, content
      print >> fd, f['content']
    else:
      try:
        c = escape_quote(f['contents'])
      except UnicodeEncodeError, e:
        print >> sys.stderr, "ERROR: %s: %s: unicode characters not supported" % (options.configchannel_label, f['path'])
      else:
        print >> fd, c
    print >> fd, "EOF__BLAH__EOF"

  print >> fd, ""
  fd.close()

client.auth.logout(key)
