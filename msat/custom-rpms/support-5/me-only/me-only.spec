Name:         me-only
Version:      1.0.0
Release:      0
Summary:      Synchronisation wrapper for bash scripts
Group:        System/Scripts
License:      GPLv3+
Source:       %{name}.tar.gz
BuildRoot:    %{_tmppath}/%{name}-root
Requires:     bash

%description
The me-only C program is a wrapper to start a shell script.
The first argument to me-only is an imaginary path on which
the run script synchronizes to make sure it it the only
instance running on a specific system.

For the imaginary path, the Linux extension to Unix domain
sockets, the abstract path, see man 7 unix, has been used.
Hence, the imaginary path is known in the kernel and is not
physically placed on the filesystem.

This way, we can not only guarantee atomicity, but also
removal (by the kernel) of the imaginary path. As a
consequence, scripts can run uniquely on a system, and, if
they crash, other scripts are not left with stale PID or
lock files.

%prep
%setup -q -n %{name}

%build
gcc -Wall -o me-only me-only.c

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/bin
mkdir -p $RPM_BUILD_ROOT/usr/share/doc/me-only
install me-only $RPM_BUILD_ROOT/usr/bin
install my-pid.sh $RPM_BUILD_ROOT/usr/share/doc/me-only
install me-only-tests.txt $RPM_BUILD_ROOT/usr/share/doc/me-only
install me-only-howto.txt $RPM_BUILD_ROOT/usr/share/doc/me-only

%clean
rm -rf $RPM_BUILD_ROOT

%post
# Empty.

%preun
# Empty.

%files
%attr(0755,root,root) /usr/bin/me-only
%doc %attr(0755,root,root) /usr/share/doc/me-only/my-pid.sh
%doc %attr(0644,root,root) /usr/share/doc/me-only/me-only-tests.txt
%doc %attr(0644,root,root) /usr/share/doc/me-only/me-only-howto.txt

%changelog
* Sun Aug 12 2012 Allard Berends <msat.disruptivefoss@gmail.com> - 1.0.0-0
- Initial creation of the RPM
