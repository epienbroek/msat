#!/usr/bin/python

#
# SCRIPT
#   list_assets.py
# DESCRIPTION
#   See the usage string in the code.
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
#   list_assets.py is free software; you can redistribute it
#   and/or modify it under the terms of the GNU General
#   Public License as published by the Free Software
#   Foundation; either version 3 of the License, or (at your
#   option) any later version.
#
#   list_assets.py is distributed in the hope that it will
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
import locale
import optparse
import os
import sys
import time
import xmlrpclib
import zipfile

OUTPUT_DIR      = '/var/log'
OUTPUT_FILE     = 'asset_lnx_satellite.txt'
OUTPUT_PATH     = os.path.join(OUTPUT_DIR, OUTPUT_FILE)
ZIP_OUTPUT_PATH = os.path.join(OUTPUT_DIR, OUTPUT_FILE + '.zip')

usage = '''usage: %prog [options]

Obtain RPM's installed on the systems, as known by the
Satellite server. Be warned: this is the Satellite view of
reality. On a system, RPM's can be added with the rpm
command. This is not seen by the Satellite.

The output is placed in a file, asset_lnx_satellite.txt, in
directory /var/log. As a consequence it must be run as root
(for /var/log).

The output of this script is as follows:
* Loop over all the known systems in Satellite
* Per system list per RPM:
  * time|node|LNX001|RPMnum|RPM|SOFTWARE-NAME|name
  * time|node|LNX001|RPMnum|RPM|SOFTWARE-VERSION|version

The fields have the following meaning:
time:             Date and time string with seconds
                  precision. For example: 18-Jun-2012
                  07:21:18
node:             hostname without the domain part.
                  Result of the cobbler setting, not of the
                  hostname command
LNX001:           Fixed tag for processing
RPMnum:           RPM is fixed. num is %0.5d according to
                  printf formatting. This results in 5
                  digits, starting with zeroes. For example,
                  RPM number 296, results in RPM00295. We
                  start counting at 0
RPM:              fixed tag to indicate that this record is
                  an RPM asset
SOFTWARE-NAME:    fixed tag for processing
name:             name of the RPM without any version,
                  release or architecture information
SOFTWARE-VERSION: fixed tag for processing
version:          version-release.architecture, as defined
                  in the RPM standard. Version and release
                  can differ per RPM. Architecture is AMD64,
                  i386, i686, or noarch. At least, that is
                  the list we have found on our Satellite.
                  In theory, the i586 and x86_64 should be
                  there too.

The default parameter file is sat.conf:
------
[satellite]
url      = http://<satellite ip or fqdn>/rpc/api
login    = <admin>
password = <admin password>
rpmpath  = /var/satellite

[cobbler]
url      = http://<satellite ip or fqdn>/cobbler_api
login    = <admin>
password = <admin password>
------

The default sat.conf is overwritten and probably best set in
.sat.conf in the home directory of the user that runs it. In
the case of this script, since it must be run as root:
/root/.sat.conf.

To run this script on a frequent basis, add it to cron with:
# cat > /etc/cron.d/nightly_rpm_assets << EOF__BLAH__EOF
# Needed for filling the CMDB with respect to software on
# the Linux nodes.
# Other tooling will pick up this file at 5.30 every
# morning.
03 05 * * * root /usr/bin/list_assets.py
EOF__BLAH__EOF
# chmod 644 /etc/cron.d/nightly_rpm_assets

Example usage:
%prog

%prog -h'''

parser = optparse.OptionParser(usage = usage)
parser.add_option(
  "-f",
  "--params-file",
  action = "callback",
  callback = config.parse_path,
  dest = "params_file",
  type = "string",
  default = '.sat.conf',
  help = "path to the parameter file. Default is ~/.sat.conf",
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

(options, args) = config.get_conf(parser)

try:
  f = open(OUTPUT_PATH, 'w')
except IOError, e:
  print >> sys.stderr, str(e)
  sys.exit(1)

# Get session key via auth namespace.
client = xmlrpclib.ServerProxy(options.satellite_url, verbose=0)
key = client.auth.login(options.satellite_login, options.satellite_password)

# Timestamp format according to IDD-BHS (Paul de Kok):
locale.setlocale(locale.LC_TIME, 'en_US')
date = time.strftime("%d-%b-%Y %H:%M:%S", time.gmtime())
try:
  systems = client.system.listSystems(
    key,
  )
except xmlrpclib.Fault, e:
  print >> sys.stderr, str(e)
  sys.exit(1)

for i in systems:
  # Obtained via HP-SIM:
  # details = client.system.getDetails(
  # details = client.system.getMemory(
  try:
    packages = client.system.listPackages(
      key,
      i['id'],
    )
  except xmlrpclib.Fault, e:
    print >> sys.stderr, str(e)
    #'release': '1', 'epoch': ' ', 'version': '2.20.005', 'arch': 'AMD64', 'name': 'HPOvAgtEx'
    sys.exit(1)
  c = 0
  for p in packages:
    s = "RPM%0.5d" % (c,)
    f.write("%s|%s|LNX001|%s|RPM|SOFTWARE-NAME|%s\n" % (date, i['name'].split('.')[0], s, p['name']))
    f.write("%s|%s|LNX001|%s|RPM|SOFTWARE-VERSION|%s\n" % (date, i['name'].split('.')[0], s, '%s-%s.%s' % (p['version'], p['release'], p['arch'])))
    c += 1

client.auth.logout(key)

f.close()

z = zipfile.ZipFile(ZIP_OUTPUT_PATH, "w")
z.write(OUTPUT_PATH, OUTPUT_FILE, zipfile.ZIP_DEFLATED)
z.close()
