#!/bin/bash
#
# SCRIPT
#   msat_ls_all_kt.sh
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
#   Allard Berends (AB), 2013-02-24 13:07
# HISTORY
# LICENSE
#   Copyright (C) 2013 Allard Berends
# 
#   msat_ls_all_kt.sh is free software; you can
#   redistribute it and/or modify it under the terms of the
#   GNU General Public License as published by the Free
#   Software Foundation; either version 3 of the License, or
#   (at your option) any later version.
#
#   msat_ls_all_kt.sh is distributed in the hope
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
  echo " -a <satellite admin>:    To overwrite the default"
  echo " -p <satellite password>: To overwrite the default"
  echo " -h : this help message"
} # end usage

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

  while getopts "a:p:h" Option 2>/dev/null
  do
    case $Option in
    a)  A_OPTION=$OPTARG ;;
    p)  P_OPTION=$OPTARG ;;
    o)  O_OPTION=$OPTARG ;;
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
  if [ -n "$A_OPTION" ]; then
    A_OPTION="-a $A_OPTION"
  fi

  # Verify P_OPTION
  if [ -n "$P_OPTION" ]; then
    P_OPTION="-p $P_OPTION"
  fi
} # end verify

# Get command line options.
options $*

# Verify command line options.
verify

for b in $(msat_ls_bc.py $A_OPTION $P_OPTION)
do
  /bin/echo "$b"
  for k in $(msat_ls_kt.py -b $b)
  do
  /bin/echo "  $k"
  done
done
