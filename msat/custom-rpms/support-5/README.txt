In this subtree one finds RPM's created by the support
department. If some other scripting or utility needs to be
added in the production environment, it must be created and
maintained in this subtree.

Since the subtree ends with "-5", these RPM's are used in
RHEL major release 5. If they need to be used for another
Linux release, they need to be recreated and placed
elsewhere. For example, in the future, a support-6 and even
a support-7 will be added here.

The list of RPM's is (and needs to be updated every time a
new one is added or one is removed):

me-only
    C program to call a script and make sure it runs
    uniquely on a system

ntp-sync
    Shell script and crontab entry to synchronise the
    hardware clock of a system to NTP

