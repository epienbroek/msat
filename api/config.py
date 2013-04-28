#!/usr/bin/python

#
# LIBRARY
#   config.py
# DESCRIPTION
# DEPENDENCIES
# FAILURE
# AUTHORS
#   Date strings made with 'date +"\%Y-\%m-\%d \%H:\%M"'.
#   Allard Berends (AB), 2013-02-24 13:07
# HISTORY
# LICENSE
#   Copyright (C) 2013 Allard Berends
# 
#   config.py is free software; you can redistribute it
#   and/or modify it under the terms of the GNU General
#   Public License as published by the Free Software
#   Foundation; either version 3 of the License, or (at your
#   option) any later version.
#
#   config.py is distributed in the hope that it will be
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

import ConfigParser
import optparse
import os
import re
import urlparse

# These parse_* functions must adhere to the callback
# definition of optparse!
def parse_url(option, opt_str, value, parser):
  u = urlparse.urlparse(value)
  #urlstring = ''.join([u.scheme, '://', u.netloc, u.path])
  urlstring = ''.join([u[0], '://', u[1], u[2]])
  if option:
    setattr(parser.values, option.dest, urlstring)
  else:
    return urlstring

def parse_path(option, opt_str, value, parser):
  p = os.path.abspath(value)
  if option:
    setattr(parser.values, option.dest, p)
  else:
    return p

def parse_file(option, opt_str, value, parser):
  if option:
    setattr(parser.values, option.dest, value)
  else:
    f = open(value)
    value = ''.join(f.readlines())
    f.close()
    return value

def parse_string(option, opt_str, value, parser):
  if option:
    setattr(parser.values, option.dest, value)
  else:
    return value

def parse_int(option, opt_str, value, parser):
  if option:
    setattr(parser.values, option.dest, value)
  else:
    return int(value)

def parse_boolean(option, opt_str, value, parser):
  if value in ['yes', 'Yes', 'YES', 'true', 'True', 'TRUE']:
    value = True
  else:
    value = False
  if option:
    setattr(parser.values, option.dest, value)
  else:
    return value

def parse_quoted_string(option, opt_str, value, parser):
  value = value.lstrip('"\'')
  value = value.rstrip('"\'')
  if option:
    setattr(parser.values, option.dest, value)
  else:
    return value
 
def print_name_purpose(p):
  print '''<refnamediv>
<refname>%(name)s</refname>
<refpurpose>%(purpose)s</refpurpose>
</refnamediv>''' % {'name': p.get_prog_name(),
'purpose': p.usage.rstrip('\n')}

def print_option(o):
  if o.dest:
    print '''  <arg choice='opt'>%(opt)s <replaceable>%(param)s</replaceable></arg>''' % {'opt': ', '.join(o._short_opts + o._long_opts), 'param': o.dest.upper()}
  else:
    print '''  <arg choice='opt'>%s</arg>''' % (', '.join(o._short_opts + o._long_opts), )

def print_synopsis(p):
  print '''<refsynopsisdiv>
<cmdsynopsis>
  <command>%s</command>''' % (p.get_prog_name(), )
  for o in p.option_list:
    print_option(o)
  print '''</cmdsynopsis>
</refsynopsisdiv>'''

def print_option_help(p, o):
  if o.help:
    help = o.help
    default_value = p.defaults.get(o.dest)
    if default_value is optparse.NO_DEFAULT or default_value is None:
      default_value = optparse.HelpFormatter.NO_DEFAULT_VALUE
    help = help.replace('%default', str(default_value))
  else:
    help = 'No text available'
  if o.dest:
    print '''    <varlistentry>
      <term><option>%(opts)s</option> <replaceable>%(param)s</replaceable></term>
      <listitem>
        <para>
          %(help)s
        </para>
      </listitem>
    </varlistentry>''' % {'opts': ', '.join(o._short_opts + o._long_opts), 'param': o.dest.upper(), 'help': help}
  else:
    print '''    <varlistentry>
      <term><option>%(opts)s</option></term>
      <listitem>
        <para>
          %(help)s
        </para>
      </listitem>
    </varlistentry>''' % {'opts': ', '.join(o._short_opts + o._long_opts), 'help': help}

def print_description(p):
  print '''<refsect1>
<title>DESCRIPTION</title>
<para>%s</para>
</refsect1>''' % (p.get_description(), )

def print_xmlhelp(option, opt_str, value, parser):
  print '''<?xml version="1.0" encoding="UTF-8" ?>
<!ENTITY %(prog)s "''' % {'prog': re.sub('\.py', '', parser.get_prog_name())}
  print_name_purpose(parser)
  print_synopsis(parser)
  print_description(parser)
  if parser.option_list:
    print '''<refsect1>
<title>OPTIONS</title>
<para>
  The options are as follows:
  <variablelist>'''
    for o in parser.option_list:
      print_option_help(parser, o)
    print '''</variablelist>
</para>
</refsect1>'''
  print '''">'''
  parser.exit()

def get_conf(parser):
  (options, args) = parser.parse_args()
  syssatconf  = '/etc/sat.conf'
  homesatconf = os.path.join(os.environ['HOME'], parser.defaults['params_file'])
  files = [syssatconf, homesatconf]
  if options.params_file not in [parser.defaults['params_file'], homesatconf, syssatconf]:
    files.append(options.params_file)
  scp = ConfigParser.SafeConfigParser()
  scp.read(files)
  for o in parser.option_list:
    if o.__dict__['dest']:
      if o.__dict__['default'] != getattr(options, o.__dict__['dest']):
        continue
      (s, p) = o.__dict__['dest'].split('_')
      if scp.has_option(s, p):
        value = o.__dict__['callback'](None, None, scp.get(s, p), None)
        setattr(options, o.__dict__['dest'], value)
  return (options,args)
