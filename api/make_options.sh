#!/bin/bash
#
# SCRIPT
#   This script is used to help generate the python code for
#   all the kickstart advanced options. It is not a
#   production script.
# DESCRIPTION
# ARGUMENTS
#   None.
# RETURN
#   0: success.
# DEPENDENCIES
# FAILURE
# AUTHORS
#   Date strings made with 'date +"\%Y-\%m-\%d \%H:\%M"'.
#   Allard Berends (AB), 2013-02-24 13:07
# HISTORY
# DESIGN
#

options="autostep interactive install upgrade text network cdrom harddrive nfs url lang langsupport keyboard mouse device deviceprobe zerombr clearpart bootloader timezone auth rootpw selinux reboot firewall xconfig skipx key ignoredisk autopart cmdline firstboot graphical iscsi iscsiname logging monitor multipath poweroff halt service shutdown user vnc zfcp"
for i in $options
do
  if [ "$i" == "interactive" ] || [ "$i" == "install" ] || [ "$i" == "upgrade" ] || [ "$i" == "text" ] || [ "$i" == "cdrom" ] || [ "$i" == "reboot" ] || [ "$i" == "skipx" ] || [ "$i" == "autopart" ] || [ "$i" == "cmdline" ] || [ "$i" == "graphical" ] || [ "$i" == "poweroff" ] || [ "$i" == "halt" ] || [ "$i" == "shutdown" ]; then
    cb="parse_boolean"
  else
    cb="parse_string"
fi
cat << EOF
  parser.add_option(
    "--kickstart-${i}",
    action   = "callback",
    callback = $cb,
    dest     = "kickstart_${i}",
    type     = "string",
    default  = None,
    help     = "$i kickstart advanced option"
  )
EOF
done

for i in $options
do
  if [ "$i" == "lang" ] || [ "$i" == "keyboard" ] || [ "$i" == "bootloader" ] || [ "$i" == "timezone" ] || [ "$i" == "auth" ] || [ "$i" == "rootpw" ]; then
    cat << EOF
if not options.kickstart_${i}:
  print >> sys.stderr, "option --kickstart-${i} is required"
  sys.exit(1)
else:
  advanced_options.append({'name':      '$i',
                           'arguments': options.kickstart_${i}})
EOF
  else
    cat << EOF
if options.kickstart_${i}:
  advanced_options.append({'name':      '$i',
                           'arguments': options.kickstart_${i}})
EOF
  fi
echo
done

for i in $options
do
  if [ "$i" == "interactive" ] || [ "$i" == "install" ] || [ "$i" == "upgrade" ] || [ "$i" == "text" ] || [ "$i" == "cdrom" ] || [ "$i" == "reboot" ] || [ "$i" == "skipx" ] || [ "$i" == "autopart" ] || [ "$i" == "cmdline" ] || [ "$i" == "graphical" ] || [ "$i" == "poweroff" ] || [ "$i" == "halt" ] || [ "$i" == "shutdown" ]; then
    cb="parse_boolean"
  else
    cb="parse_string"
fi
printf "      %-16s %s,\n" "'$i':" $cb
done

