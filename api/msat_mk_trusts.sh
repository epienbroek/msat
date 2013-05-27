#!/bin/bash
#
# SCRIPT
#   msat_mk_trusts.sh
# DESCRIPTION
# ARGUMENTS
#   None.
# RETURN
#   0: success.
# DEPENDENCIES
#   The script depends on the python Satellite API scripts.
# FAILURE
# AUTHORS
#   Date strings made with 'date +"\%Y-\%m-\%d \%H:\%M"'.
#   Allard Berends (AB), 2013-02-24 23:07
# HISTORY
# LICENSE
#   Copyright (C) 2013 Allard Berends
# 
#   msat_mk_trusts.sh is free software; you can
#   redistribute it and/or modify it under the terms of the
#   GNU General Public License as published by the Free
#   Software Foundation; either version 3 of the License, or
#   (at your option) any later version.
#
#   msat_mk_trusts.sh is distributed in the hope
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
PNAME=$(basename $0)

#
# FUNCTION
#   usage
# DESCRIPTION
#   This function explains how this script should be called
#   on the command line.
# RETURN CODE
#   Nothing
#
usage() {
  echo "Usage: $PNAME"
  echo " -a <access level>:      Must be public, private, or protected"
  echo " -l <software channels>: Comma separated list of software channels"
  echo " -o <org ids>:           Comma separated list of organization ID's"
  echo " -h : this help message"
} # end usage

#
# FUNCTION
#   xml_help
# DESCRIPTION
#   This function explains how this script should be called
#   on the command line.
# RETURN CODE
#   Nothing
#
xml_help() {
  cat << EOF__EOF
<refnamediv>
<refname>msat_mk_trusts.sh</refname>
<refpurpose>list the config channels</refpurpose>
</refnamediv>
<refsynopsisdiv>
<cmdsynopsis>
  <command>msat_mk_trusts.sh</command>
  <arg choice='opt'>-h, --help</arg>
  <arg choice='opt'>-x, --xml-help</arg>
  <arg choice='opt'>-l <replaceable>SOFTWARE_CHANNELS</replaceable></arg>
  <arg choice='opt'>-o <replaceable>ORG_IDS</replaceable></arg>
</cmdsynopsis>
</refsynopsisdiv>
<refsect1>
<title>DESCRIPTION</title>
<para>This script lists the config channels available on the Satellite server.</para>
</refsect1>
<refsect1>
<title>OPTIONS</title>
<para>
  The options are as follows:
  <variablelist>
    <varlistentry>
      <term><option>-h, --help</option></term>
      <listitem>
        <para>
          show this help message and exit
        </para>
      </listitem>
    </varlistentry>
    <varlistentry>
      <term><option>-x, --xml-help</option></term>
      <listitem>
        <para>
          Print help in XML format
        </para>
      </listitem>
    </varlistentry>
    <varlistentry>
      <term><option>-a</option> <replaceable>ACCESS_LEVEL</replaceable></term>
      <listitem>
        <para>
          must be public, private, or protected
        </para>
      </listitem>
    </varlistentry>
    <varlistentry>
      <term><option>-l</option> <replaceable>SOFTWARE_CHANNELS</replaceable></term>
      <listitem>
        <para>
          comma separated list of software channels
        </para>
      </listitem>
    </varlistentry>
    <varlistentry>
      <term><option>-o</option> <replaceable>ORG_IDS</replaceable></term>
      <listitem>
        <para>
          comma separated list of organization ID's
        </para>
      </listitem>
    </varlistentry>
</variablelist>
</para>
</refsect1>
EOF__EOF
} # end xml_help

#
# FUNCTION
#   options
# DESCRIPTION
#   This function parses the command line options.
#   If an option requires a parameter and it is not
#   given, this function exits with error code 1, otherwise
#   it succeeds. Parameter checking is done later.
# EXIT CODE
#   1: error
#
options() {
  # Assume correct processing
  RC=0

  while getopts "a:l:o:hx" Option 2>/dev/null
  do
    case $Option in
    a)  A_OPTION=$OPTARG ;;
    l)  L_OPTION=$OPTARG ;;
    o)  O_OPTION=$OPTARG ;;
    x)  xml_help
        exit 0 ;;
    ?|h|-h|-help)  usage
        exit 0 ;;
    *)  usage
        exit 1 ;;
    esac
  done

  shift $(($OPTIND-1))
  ARGS=$@
} # end options

#
# FUNCTION
#   verify
# DESCRIPTION
#   This function verifies the parameters obtained from
#   the command line.
# EXIT CODE
#   2: error
#
verify() {
  # Verify A_OPTION
  if [ -z "$A_OPTION" ]; then
      echo "ERROR: must specify -a"
      exit 2
  fi

  # Verify L_OPTION
  if [ -z "$L_OPTION" ]; then
      echo "ERROR: must specify -l"
      exit 2
  fi

  # Verify O_OPTION
  if [ -z "$O_OPTION" ]; then
      echo "ERROR: must specify -o"
      exit 2
  fi
} # end verify

# Get command line options.
options $*

# Verify command line options.
verify

# AB: loop over de software channels
for i in $(/bin/echo $O_OPTION | /usr/bin/tr ',' ' ')
do
  echo "msat_mk_org_trust.py -o $i"
  msat_mk_org_trust.py -o $i
  for s in $(/bin/echo $L_OPTION | /usr/bin/tr ',' ' ')
  do
    echo "msat_mk_sc_org.py -t yes -s $A_OPTION -l $s -o $i"
    msat_mk_sc_org.py -t yes -s $A_OPTION -l $s -o $i
  done
done

