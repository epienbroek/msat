#!/bin/bash
#
# SCRIPT
#   msat_cmds_list.sh
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
#   Allard Berends (AB), 2013-05-25 14:36
# HISTORY
# LICENSE
#   Copyright (C) 2013 Allard Berends
# 
#   msat_cmds_list.sh is free software; you can
#   redistribute it and/or modify it under the terms of the
#   GNU General Public License as published by the Free
#   Software Foundation; either version 3 of the License, or
#   (at your option) any later version.
#
#   msat_cmds_list.sh is distributed in the hope
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

API=/home/allard/projects/prorail/msat/api

ls $API/msat_*.py $API/msat_*.sh | sed 's#^.*/##' | sed 's#\(.*\)\..*$#<xi:include href="references/\1.xml" xmlns:xi="http://www.w3.org/2001/XInclude" />#'
