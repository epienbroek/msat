#!/bin/bash
#
# SCRIPT
#   msat_rm_kp_hy.sh
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
#   Gerben Welter (GW), 2013-08-02 10:27
# HISTORY
# LICENSE
#   Copyright (C) 2013 Allard Berends
#
#   msat_rm_kp_hy.sh is free software; you can
#   redistribute it and/or modify it under the terms of the
#   GNU General Public License as published by the Free
#   Software Foundation; either version 3 of the License, or
#   (at your option) any later version.
#
#   msat_rm_kp_hy.sh is distributed in the hope
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
  echo " -h : this help message"
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
<refname>msat_rm_kp_hy.sh</refname>
<refpurpose>removes kickstart profile and hierarchy below except common activations keys and config channels in the current satellite organisation</refpurpose>
</refnamediv>
<refsynopsisdiv>
<cmdsynopsis>
  <command>msat_rm_kp_hy.sh</command>
  <arg choice='opt'>-h, --help</arg>
  <arg choice='opt'>-l, --label</arg>
  <arg choice='opt'>-x, --xml-help</arg>
</cmdsynopsis>
</refsynopsisdiv>
<refsect1>
<title>DESCRIPTION</title>
<para>This script removes kickstart profile and hierarchy below except common activations keys and config channels in the current satellite organisation.</para>i
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
      <term><option>-l, --label</option></term>
      <listitem>
        <para>
          kickstart label
        </para>
      </listitem>
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

  while getopts "l:hx" Option 2>/dev/null
  do
    case $Option in
    l)  L_OPTION=$OPTARG ;;
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
  # Verify L_OPTION
  if [ -z "$L_OPTION" ]; then
    echo "ERROR: Kickstart profile not supplied!"
    echo "Use the -l option to supply the kickstart profile."
    exit 2
  fi

  if [ -n "$ARGS" ]; then
    echo "ERROR: extra \"$ARGS\" found"
    exit 2
  fi
} # end verify

# Get command line options.
options $*

# Verify command line options.
verify

# Verify existance of Kickstart profile
msat_ls_kp.py | grep -q ^${L_OPTION}\$
RC=$?

if [ "$RC" != 0 ]; then
	echo "ERROR: supplied kickstart label cannot be found!"
	exit 1
fi

# Get ORG id to use in the Activation Key
ORGNUM=$(msat_ls_org.py)

# Deduce name of Activation Key to remove
# AB: the naming convetion of a kp dictates:
#     <name>-<r>u<m>-<x_y_z>, where:
#     <name>: name of the app
#     <r>: RHEL major, minimally a one-digit number
#     <m>: RHEL minor, minimally a one-digit number
#     <x_y_z>: tag release, e.g. 1_0 or 5_8_3.
# The app type ak is:
#     <orgnum>-<name>-<r>u<m>-<x_y_z>. Here we assume that
#     an app version propagates to the kp, ak, cc (of the
#     app) version.
# Since the '-' character may be part of the <name>, we can
# only deduce the name by chopping of the part
# -<r>u<m>-<x_y_z>.
#
# GW: Only we also want to be able to split the machine type
#     from the name so we can delete both the generic application
#     config channel and the machine specific
#     application config channel. This why the out put from sed
#     is split again, keeping in mind that the application
#     name may also contain the '-' character. With AK_NAME
#     we additionally need to strip the extra '-' character
#     because awk always prints the FS even if $NF is made empty.
AK_NAME=$(echo ${L_OPTION} | sed 's/-[0-9]\{1,\}w\?u[0-9]\{1,\}.*$//' | awk 'BEGIN{FS="-";OFS="-"}{$NF=""; print $0}' | sed 's/.$//')
AK_MACH=$(echo ${L_OPTION} | sed 's/-[0-9]\{1,\}w\?u[0-9]\{1,\}.*$//' | awk 'BEGIN{FS="-"}{print $NF}')
AK_VERSION=$(echo ${L_OPTION} | sed 's/^.*-[0-9]\{1,\}w\?u[0-9]\{1,\}-//')

# Deduce name of Config Channel to remove
#RHEL_MAJOR=$(echo $L_OPTION | cut -f3 -d- | cut -c2)
# AB: deducing major version is not 100%. One can have
# <number>u in the app name!
RHEL_MAJOR=$(echo ${L_OPTION} | sed 's/^.*-\([0-9]\{1,\}w\?\)u[0-9]\{1,\}-.*/\1/')
CC_NAME="${AK_NAME}-${RHEL_MAJOR}-${AK_VERSION}"
CC_MACH="${AK_NAME}-${AK_MACH}-${RHEL_MAJOR}-${AK_VERSION}"

# Removing the hierarchy from top to bottom

echo "Removing kickstart profile ${L_OPTION} and its hierarchy."
echo "Leaving generic Activation Keys and Config Channels intact."
echo "==========================================================="
echo "Removing Kickstart profile ${L_OPTION}."
msat_rm_kp.py -l ${L_OPTION}
echo "Removing Activation Key ${ORGNUM}-${L_OPTION}."
msat_rm_ak.py -l ${ORGNUM}-${L_OPTION}
echo "Removing Configuration Channel ${CC_NAME}."
msat_rm_cc.py -l ${CC_NAME}
echo "Removing machine specific Configuration Channel ${CC_MACH}."
msat_rm_cc.py -l ${CC_MACH}

