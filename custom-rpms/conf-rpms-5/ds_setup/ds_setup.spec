Name:		    ds_setup
Version:    1.0.0
Release:    0
Summary:    Directory server node specific setup file
Group:	    System/Scripts
License:    GPLv3+
Requires:   bash
Source:     %{name}.tar.gz
BuildRoot:  %{_tmppath}/%{name}-root

%description
This software package has no contents. The package is merely
used to create a directory server setup file during
installation.

What is configured?
FullMachineName = ds1.dmsat1.org
AdminDomain = dmsat1.org
ConfigDirectoryLdapURL = ldap://ds1.dmsat1.org:389/o=NetscapeRoot
ServerIdentifier = ds1
Suffix = dc=dmsat1,dc=org
ServerIpAddress = 192.168.5.14

%prep
%setup -q -n %{name}

%build
# Empty. Since no compilation or else is needed.

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/share/doc/%{name}
mkdir -p $RPM_BUILD_ROOT/root
install README $RPM_BUILD_ROOT/usr/share/doc/%{name}
install setup.inf $RPM_BUILD_ROOT/root

%clean

%pre
# Empty.

%post
THIS_HOST=$(/bin/hostname -s)
THIS_DOMAIN=$(/bin/dnsdomainname)
DC1=${THIS_DOMAIN%%.*}
DC2=${THIS_DOMAIN#*.}
IP=$(/bin/hostname --ip-address)

/bin/sed -i \
  -e "s/^FullMachineName = .*$/FullMachineName = $THIS_HOST.$THIS_DOMAIN/" \
  -e "s/^AdminDomain = .*$/AdminDomain = $THIS_DOMAIN/" \
  -e "s#^ConfigDirectoryLdapURL = .*$#ConfigDirectoryLdapURL = ldap://$THIS_HOST.$THIS_DOMAIN:389/o=NetscapeRoot#" \
  -e "s/^ServerIdentifier = .*$/ServerIdentifier = $THIS_HOST/" \
  -e "s/^Suffix = .*$/Suffix = dc=$DC1,dc=$DC2/" \
  -e "s/^ServerIpAddress = .*$/ServerIpAddress = $IP/" \
  /root/setup.inf

%preun

%postun
# Empty.

%files
%doc %attr(0644,root,root) /usr/share/doc/%{name}/README
%attr(0644,root,root) /root/setup.inf

%changelog
* Sun Jun 23 2013 Allard Berends <msat.disruptivefoss@gmail.com> - 1.0.0-0
- Initial creation of the RPM
