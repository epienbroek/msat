#!/bin/bash
RPM=me-only
tar -cz --exclude=.svn -f ~/rpm/SOURCES/${RPM}.tar.gz ${RPM}
rpmbuild --target x86_64 --clean -bb ${RPM}.spec
RC=$?
if [ $RC -ne 0 ]; then
  echo "ERROR: rpmbuild failed with exit code: $RC"
fi
rm ~/rpm/SOURCES/${RPM}.tar.gz
exit $RC
