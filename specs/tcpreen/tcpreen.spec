# Authority: dag

Summary: TCP/IP re-engineering and monitoring program.
Name: tcpreen
Version: 1.3.7
Release: 1
License: GPL
Group: Applications/Internet
URL: http://www.simphalempin.com/dev/tcpreen/

Packager: Dag Wieers <dag@wieers.com>
Vendor: Dag Apt Repository, http://dag.wieers.com/apt/

Source: http://dl.sf.net/tcpreen/tcpreen-%{version}.tar.bz2
BuildRoot: %{_tmppath}/root-%{name}-%{version}
Prefix: %{_prefix}

%description
A tool to monitor and analyse data transmitted between a client and a server
via a TCP connection. This tool focuses on the data stream (software layer),
not on the lower level transmission protocol as packet sniffers do.

TCPreen supports both TCP/IPv4 and TCP/IPv6 for data transport.

%prep
%setup

%build
%configure
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%makeinstall
%find_lang %{name}

%clean
%{__rm} -rf %{buildroot}

%files -f %{name}.lang
%defattr(-, root, root, 0755)
%doc AUTHORS ChangeLog COPYING NEWS README THANKS TODO
%doc %{_mandir}/man?/*
%{_bindir}/*

%changelog
* Wed Mar 03 2004 Dag Wieers <dag@wieers.com> - 1.3.7-1
- Updated to release 1.3.7.

* Sun Nov 23 2003 Dag Wieers <dag@wieers.com> - 1.3.6-0
- Updated to release 1.3.6.

* Mon Oct 06 2003 Dag Wieers <dag@wieers.com> - 1.3.5-0
- Initial package. (using DAR)
