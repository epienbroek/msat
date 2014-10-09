Name:		      ntp-sync
Version:    	1.0.0
Release:    	0
Summary:    	NTP to hardware clock synchronisation
Group:	    	System/Scripts
License:    	GPLv3+
Requires:   	bash
Source:       %{name}.tar.gz
BuildRoot:    %{_tmppath}/%{name}-root

%description
This packages provides a script that synchronizes the NTP
system time to the hardware clock, after testing that NTP is
correct.

%prep
%setup -q -n %{name}

%build
# Empty. Since no compilation or else is needed.

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/bin
mkdir -p $RPM_BUILD_ROOT/etc/cron.d
install %{name}.sh $RPM_BUILD_ROOT/usr/bin
install %{name} $RPM_BUILD_ROOT/etc/cron.d

%clean

%pre
# Empty.

%post
# Empty.

%preun
# Empty.

%postun
# Empty.

%files
%attr(0755,root,root) /usr/bin/%{name}.sh
%config %attr(0644,root,root) /etc/cron.d/%{name}

%changelog
* Sat Apr 20 2013 Allard Berends <msat.disruptivefoss@gmail.com> - 1.0.0-0
- Initial creation of the RPM
