# Authority: dag

# Upstream: Todor T. Zviskov <warder@warder.ath.cx>

Summary: A Video-For-Linux frontend of transcode.
Name: gv4l
Version: 2.2.2
Release: 0
License: GPL
Group: Applications/Multimedia
URL: http://gv4l.sourceforge.net/

Packager: Dag Wieers <dag@wieers.com>
Vendor: Dag Apt Repository, http://dag.wieers.com/apt/

Source: http://dl.sf.net/gv4l/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/root-%{name}-%{version}
Prefix: %{_prefix}

BuildRequires: libgnomeui-devel >= 2.0
Requires: transcode >= 0.6.7, xawtv

%description
Gv4l is a gui frontend for the v4l (Video For Linux) functions of transcode.

%prep
%setup

%build
%configure
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%makeinstall

### FIXME: The default gv4l desktop file has buildroot in it. (Please fix upstream)
%{__cat} <<EOF >%{name}.desktop
[Desktop Entry]
Name=Gv4l Video Recorder
Comment=A Video-For-Linux frontend for transcode
Icon=gv4l/gv4l.png
Exec=gv4l
Terminal=false
Type=Application
Categories=GNOME;Application;AudioVideo;
EOF

desktop-file-install --vendor gnome                \
	--add-category X-Red-Hat-Base              \
	--dir %{buildroot}%{_datadir}/applications \
	%{name}.desktop

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%{_bindir}/*
%{_datadir}/pixmaps/gv4l/
%{_datadir}/applications/*.desktop

%changelog
* Fri Jan 02 2004 Dag Wieers <dag@wieers.com> - 2.2.2-0
- Updated to release 2.2.2.

* Thu Dec 04 2003 Dag Wieers <dag@wieers.com> - 2.1.0-1
- Re-added desktop file. (Alfredo Milani-Comparetti)

* Mon Sep 08 2003 Dag Wieers <dag@wieers.com> - 2.1.0-0
- Updated to release 2.1.0.

* Tue Sep 02 2003 Dag Wieers <dag@wieers.com> - 2.0.2-0
- Updated to release 2.0.2.

* Sun Jul 13 2003 Dag Wieers <dag@wieers.com> - 2.0.1-0
- Updated to release 2.0.1.

* Thu Jul 03 2003 Dag Wieers <dag@wieers.com> - 2.0.0-0
- Updated to release 2.0.0.

* Wed Feb 12 2003 Dag Wieers <dag@wieers.com> - 1.91-1
- Added .desktop file.

* Sun Jan 19 2003 Dag Wieers <dag@wieers.com> - 1.91-0
- Initial package. (using DAR)
