#!/bin/bash
#
# SCRIPT
#   msat_rm_cb_all.sh
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
#   Allard Berends (AB), 2013-03-14 14:59
# HISTORY
# LICENSE
#   Copyright (C) 2013 Allard Berends
# 
#   msat_rm_cb_all.sh is free software; you can
#   redistribute it and/or modify it under the terms of the
#   GNU General Public License as published by the Free
#   Software Foundation; either version 3 of the License, or
#   (at your option) any later version.
#
#   msat_rm_cb_all.sh is distributed in the hope
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

COBBLER="sudo cobbler"

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
  echo " -x : XML help for manpage generation"
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
<refname>msat_rm_cb_all.sh</refname>
<refpurpose>removes all cobbler systems</refpurpose>
</refnamediv>
<refsynopsisdiv>
<cmdsynopsis>
  <command>msat_rm_cb_all.sh</command>
  <arg choice='opt'>-h, --help</arg>
  <arg choice='opt'>-x, --xml-help</arg>
</cmdsynopsis>
</refsynopsisdiv>
<refsect1>
<title>DESCRIPTION</title>
<para>This script removes all Cobbler systems.</para>
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

  while getopts "hx" Option 2>/dev/null
  do
    case $Option in
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

# Get command line options.
options $*

$COBBLER system list | while read line
do
  $COBBLER system remove --name $line
done
