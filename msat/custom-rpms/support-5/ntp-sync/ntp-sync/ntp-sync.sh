#!/bin/bash
#
# SCRIPT
#   ntp-sync.sh
# DESCRIPTION
#   Systems must use NTP to keep track of time. When the NTP
#   service is down, systems must rely on their internal
#   clock. Hence, the internal clock must be synchronised to
#   NTP. This is done once a day via this script, run from
#   cron. The name of the crontab entry is ntp-sync.
#
#   The script must only synchronise if we know that NTP is
#   correct. Hence, this is first checked with ntpq.
#
#   The cron entry is placed in /etc/cron.d and looks like:
#   53 03 * * * root /root/ntp-sync.sh
# ARGUMENTS
#   None.
# RETURN
#   0: success.
# DEPENDENCIES
# FAILURE
# AUTHORS
#   Date strings made with date +"\%Y-\%m-\%d \%H:\%M".
#   Allard Berends (AB), 2013-04-20 14:16
# HISTORY
# LICENSE
#   Copyright (C) 2013 Allard Berends
#
#   ntp-sync.sh is free software; you can
#   redistribute it and/or modify it under the terms of the
#   GNU General Public License as published by the Free
#   Software Foundation; either version 3 of the License, or
#   (at your option) any later version.
#
#   ntp-sync.sh is distributed in the hope that it
#   will be useful, but WITHOUT ANY WARRANTY; without even
#   the implied warranty of MERCHANTABILITY or FITNESS FOR A
#   PARTICULAR PURPOSE. See the GNU General Public License
#   for more details.
#
#   You should have received a copy of the GNU General
#   Public License along with this program; if not, write to
#   the Free Software Foundation, Inc., 59 Temple Place -
#   Suite 330, Boston, MA 02111-1307, USA.
# DESIGN
#   Reason for this script to exist is that we don not want
#   to rely on an initial install once to set the hardware
#   clock. In case of NTP failure, we want to have an
#   accurate hardware time. So, we synchronise on a daily
#   basis.
#   Furthermore, if we rely on the installation to set the
#   hardware clock from NTP and NTP is not available, we do
#   not even start out with a correctly set hardware clock.

GREP=/bin/grep
HWCLOCK=/sbin/hwclock
NTPQ=/usr/sbin/ntpq

# Test if we have a sys.peer (see man ntpq) upstream NTP
# server.
$NTPQ -n -p | $GREP "^\*" >/dev/null 2>&1 || { echo "ERROR: no NTP time" 1>&2; exit 1; }

# Set the hardware clock to the system time.
$HWCLOCK --systohc --utc
