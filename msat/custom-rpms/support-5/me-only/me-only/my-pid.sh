#!/bin/bash
#
# SCRIPT
#   my-pid.sh
# DESCRIPTION
# ARGUMENTS
#   None.
# RETURN
#   0: success.
# DEPENDENCIES
# FAILURE
# AUTHORS
#   Date strings made with 'date +"\%Y-\%m-\%d \%H:\%M"'.
#   Allard Berends (AB), 2012-01-16 17:17
# HISTORY
# LICENSE
#   Copyright (C) 2012 Allard Berends
#   Copyright (C) 2013 Allard Berends
# 
#   my-pid.sh is free software; you can redistribute it
#   and/or modify it under the terms of the GNU General
#   Public License as published by the Free Software
#   Foundation; either version 3 of the License, or (at your
#   option) any later version.
#
#   my-pid.sh is distributed in the hope that it will be
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

i=0
while [ $i -lt $1 ]
do
  echo -n "running $$ "
  i=$(($i + 1))
done
