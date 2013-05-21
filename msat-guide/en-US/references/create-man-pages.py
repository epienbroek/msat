#!/usr/bin/python
#
# SCRIPT
#   create-man-pages.py
# DESCRIPTION
# DEPENDENCIES
# FAILURE
# AUTHORS
#   Date strings made with 'date +"\%Y-\%m-\%d \%H:\%M"'.
#   Allard Berends (AB), 2013-05-20 17:41
# HISTORY
# LICENSE
#   Copyright (C) 2013 Allard Berends
# 
#   create-man-pages.py is free software; you can
#   redistribute it and/or modify it under the terms of the
#   GNU General Public License as published by the Free
#   Software Foundation; either version 3 of the License, or
#   (at your option) any later version.
#
#   create-man-pages.py is distributed in the hope
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

import os
import re
import subprocess
import sys

MSAT_SCRIPTS_DIR = '/home/allard/projects/prorail/msat/api'

includeline = re.compile('^@msat_command@')
direntries = os.listdir('.')
direntries = [x for x in direntries if x.endswith('.src')]
for f in direntries:
  g = re.sub('\.src', '.xml', f)
  fp = open(f, 'r')
  gp = open(g, 'w')
  while True:
    line = fp.readline()
    if not line:
      break
    m = includeline.search(line)
    if m:
      h = re.sub('\.src', '.py', f)
      hp = subprocess.Popen([os.path.join(MSAT_SCRIPTS_DIR, h), '--xml-help'], stdout=subprocess.PIPE, stderr=None).stdout
      while True:
        l = hp.readline()
        if not l:
          break
        gp.write(l)
      hp.close()
    else:
      gp.write(line)
  fp.close()
  gp.close()
