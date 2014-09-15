#!/usr/bin/python

#
# SCRIPT
#   msat_wr_cb_sys.py
# DESCRIPTION
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
#   msat_wr_cb_sys.py is free software; you can
#   redistribute it and/or modify it under the terms of the
#   GNU General Public License as published by the Free
#   Software Foundation; either version 3 of the License, or
#   (at your option) any later version.
#
#   msat_wr_cb_sys.py is distributed in the hope
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
import xmlrpclib

def print_header(name, pip, cip, iip, nameservers):
  date = time.strftime('%Y-%m-%d %H:%M', time.gmtime())
  sys.stdout.write('''#!/bin/bash
#
# SCRIPT
#   cobbler_%(name)s.sh
# DESCRIPTION
#   This script should be run on the Satellite server:
#   # ./cobbler_%(name)s.sh
#
#   IP details
#
#   Host            Prod            Cluster         ILO
#   %(name)-16.16s%(pip)-16.16s%(cip)-16.16s%(iip)-16.16s
#
#   DNS servers:
''' % {'name': name, 'pip': pip, 'cip': cip, 'iip': iip})

  for n in nameservers:
    sys.stdout.write('''#   * %s
''' % (n, ))

  sys.stdout.write('''# ARGUMENTS
#   None.
# RETURN
#   Value from cobbler command. See cobbler man page.
# DEPENDENCIES
#   The profile should not yet exist in cobbler. If it does,
#   remove it with:
#   cobbler system remove --name=%s
#   Adding an existing profile results in a clear warning
#   from cobbler. No harm is done.
# FAILURE
# AUTHORS
#   Date strings made with 'date +"\\%%Y-\\%%m-\\%%d \\%%H:\\%%M"'.
#   Allard Berends (AB), %s
# HISTORY
# LICENSE
#   Copyright (C) 2013 Allard Berends
#
#   cobbler_%s.sh is free software; you can
#   redistribute it and/or modify it under the terms of the
#   GNU General Public License as published by the Free
#   Software Foundation; either version 3 of the License, or
#   (at your option) any later version.
#
#   cobbler_%s.sh is distributed in the hope
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

########## PARAMETERS TO EDIT ##########
''' % (name, date, name, name))

def print_parameters(d, pip, psub, cip, csub, cdns, eths):
  m = re.search('([^:]+):([^:]+):([^:]+)', d['profile'])
  profile = m.group(1)
  orgnum  = m.group(2)
  org     = m.group(3)
  sys.stdout.write('''NAME=%(name)s
OWNERS="%(owners)s"
PROFILE="%(profile)s"
ORG="%(org)s"
ORG_NUMBER=%(orgnum)s
COMMENT="%(comment)s"
GATEWAY=%(gateway)s
NAMESERVERS="%(nameservers)s"
NAMESERVERS_SEARCH="%(nameserver_search)s"
HOSTNAME=${NAME}.${NAMESERVERS_SEARCH}
PROD_IP=%(pip)s
PROD_SUBNET=%(psub)s
PROD_DNS_NAME=${HOSTNAME}
''' % {
  'name':              d['name'],
  'owners':            ' '.join(d['owners']),
  'profile':           profile,
  'org':               org,
  'orgnum':            orgnum,
  'comment':           d['comment'],
  'gateway':           d['gateway'],
  'nameservers':       ' '.join(d['name_servers']),
  'nameserver_search': ' '.join(d['name_servers_search']),
  'pip':               pip,
  'psub':              psub
})
  if not cip == '-':
    print 'CLUSTER_IP=%s' % (cip,)
    print 'CLUSTER_SUBNET=%s' % (csub,)
    print 'CLUSTER_DNS_NAME=${NAME}.cluster.${NAMESERVERS_SEARCH}'
  else:
    print '#CLUSTER_IP='
    print '#CLUSTER_SUBNET='
    print '#CLUSTER_DNS_NAME='
  i = 0
  for mac in [d['interfaces'][m]['mac_address'] for m in d['interfaces'].keys() if m.startswith('eth')]:
    print 'MAC_ETH%d=%s' % (i, mac)
    i += 1
  print

def print_system(d):
  sys.stdout.write('''########## START SCRIPT ##########
cobbler system add \\
  --name=${NAME} \\
  --owners=${OWNERS} \\
  --profile=${PROFILE}:${ORG_NUMBER}:${ORG} \\
  --kopts="ksdevice=${MAC_ETH0} console=ttyS0,115200n8" \\
  --netboot-enabled=0 \\
  --comment=${COMMENT} \\
  --power-type=ipmitool \\
  --hostname=${HOSTNAME} \\
  --gateway=${GATEWAY} \\
  --name-servers="$NAMESERVERS" \\
  --name-servers-search=$NAMESERVERS_SEARCH \\
  --redhat-management-key='<<inherit>>' \\
  --redhat-management-server='<<inherit>>'
  #--uid=UID
  #--image=IMAGE
  #--kopts-post=KOPTS_POST
  #--ksmeta=KSMETA
  #--kickstart=KICKSTART
  #--depth=DEPTH
  #--server=SERVER
  #--virt-path=VIRT_PATH
  #--virt-type=VIRT_TYPE
  #--virt-cpus=VIRT_CPUS
  #--virt-file-size=VIRT_FILE_SIZE
  #--virt-ram=VIRT_RAM
  #--virt-auto-boot=VIRT_AUTO_BOOT
  #--ctime=CTIME
  #--mtime=MTIME
  #--power-address=POWER_ADDRESS
  #--power-user=POWER_USER
  #--power-pass=POWER_PASS
  #--power-id=POWER_ID
  #--ipv6-default-device=IPV6_DEFAULT_DEVICE
  #--ipv6-autoconfiguration=IPV6_AUTOCONFIGURATION
  #--mgmt-classes=MGMT_CLASSES
  #--template-files=TEMPLATE_FILES
  #--template-remote-kickstarts=TEMPLATE_REMOTE_KICKSTARTS
  #--clobber
  #--template-files=TEMPLATE_FILES
  #--in-place

''')

def print_eth_bond(name, eth, e):
  sys.stdout.write('''cobbler system edit \\
  --name=${NAME} \\
  --mac-addres="${MAC_%(mac)s}" \\
  --bonding=slave \\
  --bonding-master=%(bonding_master)s \\
  --interface=%(eth)s

''' % {
  'name':           name,
  'eth':            eth,
  'mac':            eth.upper(),
  'bonding':        e['bonding'],
  'bonding_master': e['bonding_master'],
})

def print_eth(name, eth, e):
  sys.stdout.write('''cobbler system edit \\
  --name=${NAME} \\
  --mac-address="${MAC_%(mac)s}" \\
  --ip-address=${PROD_IP} \\
  --static=1 \\
  --subnet=${PROD_SUBNET} \\
  --dns-name=${PROD_DNS_NAME} \\
  --interface=%(eth)s
  #--mtu=MTU
  #--bonding=BONDING
  #--bonding-master=BONDING_MASTER
  #--bonding-opts=BONDING_OPTS
  #--dhcp-tag=DHCP_TAG
  #--static-routes=STATIC_ROUTES
  #--virt-bridge=VIRT_BRIDGE
  #--ipv6-address=IPV6_ADDRESS
  #--ipv6-secondaries=IPV6_SECONDARIES
  #--ipv6-mtu=IPV6_MTU
  #--ipv6-static-routes=IPV6_STATIC_ROUTES
  #--ipv6-default-gateway=IPV6_DEFAULT_GATEWAY

''' % {
  'name':     name,
  'eth':      eth,
  'mac':      eth.upper(),
  'ip':       e['ip_address'],
  'subnet':   e['subnet'],
  'dns_name': e['dns_name'],
  'dhcp_tag': e['dhcp_tag'],
})

def print_bond(name, bond, b):
  if bond == 'bond0':
    ip       = '${PROD_IP}'
    subnet   = '${PROD_SUBNET}'
    mac      = '${MAC_ETH0}'
    dns_name = '${PROD_DNS_NAME}'
  else:
    ip       = '${CLUSTER_IP}'
    subnet   = '${CLUSTER_SUBNET}'
    mac      = '${MAC_ETH1}'
    dns_name = '${CLUSTER_DNS_NAME}'

  sys.stdout.write('''cobbler system edit \\
  --name=%(name)s \\
  --mac-address="%(mac)s" \\
  --ip-address=%(ip)s \\
  --static=1 \\
  --bonding=master \\
  --bonding-opts="%(bonding_opts)s" \\
  --subnet=%(subnet)s \\
  --dns-name=%(dns_name)s \\
  --dhcp-tag=%(dhcp_tag)s \\
  --interface=%(bond)s
  #--mtu=MTU
  #--bonding=BONDING
  #--bonding-master=BONDING_MASTER
  #--bonding-opts=BONDING_OPTS
  #--dhcp-tag=DHCP_TAG
  #--static-routes=STATIC_ROUTES
  #--virt-bridge=VIRT_BRIDGE
  #--ipv6-address=IPV6_ADDRESS
  #--ipv6-secondaries=IPV6_SECONDARIES
  #--ipv6-mtu=IPV6_MTU
  #--ipv6-static-routes=IPV6_STATIC_ROUTES
  #--ipv6-default-gateway=IPV6_DEFAULT_GATEWAY

''' % {
  'name':         name,
  'bond':         bond,
  'mac':          mac,
  'bonding_opts': b['bonding_opts'],
  'ip':           ip,
  'subnet':       subnet,
  'dns_name':     dns_name,
  'dhcp_tag':     '${DHCP_TAG}'
})

usage = '''list activation keys'''

description = '''This script lists the activation keys on the specified Satellite server.'''

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
  help = "path to the parameter file. Default is ~/.sat.conf",
)

parser.add_option(
  "-u",
  "--cobbler-url",
  action = "callback",
  callback = config.parse_url,
  dest = "cobbler_url",
  type = "string",
  default = None,
  help = "Satellite RPC API URL to use",
)
parser.add_option(
  "-a",
  "--cobbler-login",
  action = "callback",
  callback = config.parse_string,
  dest = "cobbler_login",
  type = "string",
  default = None,
  help = "admin account to log in with on Satellite",
)
parser.add_option(
  "-p",
  "--cobbler-password",
  action = "callback",
  callback = config.parse_string,
  dest = "cobbler_password",
  type = "string",
  default = None,
  help = "password belonging to Satellite admin account",
)
parser.add_option(
  "-n",
  "--cobbler-name",
  action = "callback",
  callback = config.parse_string,
  dest = "cobbler_name",
  type = "string",
  default = None,
  help = "name of the system to save",
)

(options, args) = config.get_conf(parser)

if options.cobbler_name is None:
  parser.error('specify cobbler name, -n or --cobbler-name. Use cobbler system list to find all system names.')

# Get session key via auth namespace.
client = xmlrpclib.ServerProxy(options.cobbler_url, verbose=0)
key = client.login(options.cobbler_login, options.cobbler_password)

try:
  system = client.get_system(options.cobbler_name)
except xmlrpclib.Fault, e:
  print >> sys.stderr, str(e)
  sys.exit(1)

if str(system) == '~':
  print "%s does not exist" % (options.cobbler_name,)
  sys.exit(0)

bonds = [k for k in system['interfaces'].keys() if k.startswith('bond')]
if bonds: bonds.sort()
eths = [e for e in system['interfaces'].keys() if e.startswith('eth')]
if eths: eths.sort()

if bonds:
  # AB: pip == production ip
  pip  = system['interfaces'][bonds[0]]['ip_address']
  psub = system['interfaces'][bonds[0]]['subnet']
  pdns = system['interfaces'][bonds[0]]['dns_name']
  try:
    # AB: cip == cluster ip
    cip  = system['interfaces'][bonds[1]]['ip_address']
    csub = system['interfaces'][bonds[1]]['subnet']
    cdns = system['interfaces'][bonds[1]]['dns_name']
  except IndexError, e:
    cip  = '-'
    csub = '-'
    cdns = '-'
else:
  pip  = system['interfaces'][eths[0]]['ip_address']
  psub = system['interfaces'][eths[0]]['subnet']
  pdns = system['interfaces'][eths[0]]['dns_name']
  cip  = '-'
  csub = '-'
  cdns = '-'

print_header(system['name'], pip, cip, '-', system['name_servers'])
print_parameters(system, pip, psub, cip, csub, cdns, eths)
print_system(system)

if bonds:
  for e in eths:
    print_eth_bond(system['name'], e, system['interfaces'][e])
  for b in bonds:
    print_bond(system['name'], b, system['interfaces'][b])
else:
  for e in eths:
    print_eth(system['name'], e, system['interfaces'][e])

client.logout(key)

