# Authority: dag
# Upstream: Alexandre Parenteau <aubonbeurre@hotmail.com>
# Distcc: 0

### FIXME: Modified to co-exist with cvs. (Please fix upstream)

%define dfi %(which desktop-file-install &>/dev/null; echo $?)

Summary: GUI interface for CVS.
Name: gcvs
Version: 1.0
Release: 1
License: GPL
Group: Development/Tools
URL: http://cvsgui.sourceforge.net/

Packager: Dag Wieers <dag@wieers.com>
Vendor: Dag Apt Repository, http://dag.wieers.com/apt/

Source: http://dl.sf.net/cvsgui/gcvs-%{version}.tar.bz2
BuildRoot: %{_tmppath}/root-%{name}-%{version}
Prefix: %{_prefix}

BuildRequires: gtk+-devel
%{?rhfc1:BuildRequires: tcl-devel}
%{?rhel3:BuildRequires: tcl-devel}
BuildRequires: tcl

#Obsoletes: cvs

%description
The gcvs package contains an interface for cvs written in C++ using
gtk+. It contains a version of cvs modified for communication
purposes with gcvs. gcvs is part of a bigger project named CvsGui
which provides several graphical clients on Mac and Windows as well.

%prep
%setup

%{__cat} <<EOF >%{name}.desktop
[Desktop Entry]
Name=gcvs
Comment=Gcvs CVS Browser
Icon=gnome-util.png 
Exec=gcvs
Type=Application
Terminal=false
EOF

%{__mv} -f cvsunix/man/cvs.1 cvsunix/man/cvs-gcvs.1
%{__mv} -f cvsunix/man/cvs.5 cvsunix/man/cvs-gcvs.5
%{__mv} -f cvsunix/man/cvsbug.8 cvsunix/man/cvsbug-gcvs.8
for i in $(seq 1 9); do
	%{__mv} -f cvsunix/doc/cvs.info-$i cvsunix/doc/cvs-gcvs.info-$i
	%{__mv} -f cvsunix/doc/cvsclient.info-$i cvsunix/doc/cvsclient-gcvs.info-$i
done

%build
CFLAGS="%{optflags}" ./make_configure \
	--disable-dependency-tracking \
	--prefix="%{_prefix}" \
	--bindir="%{_bindir}" \
	--libdir="%{_libdir}" \
	--mandir="%{_mandir}" \
	--infodir="%{_infodir}" \
	--datadir="%{_datadir}"
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%makeinstall \
	MANFILES="cvs-gcvs.1 cvs-gcvs.5 cvsbug-gcvs.8"

### Clean up buildroot (get rid of conflicting files with cvs package)
%{__rm} -rf %{buildroot}%{_infodir}

%if %{dfi}
	%{__install} -d -m0755 %{buildroot}%{_datadir}/gnome/apps/Utilities/
	%{__install} -m0644 %{name}.desktop %{buildroot}%{_datadir}/gnome/apps/Utilities/
%else
	%{__install} -d -m0755 %{buildroot}%{_datadir}/applications
	desktop-file-install --vendor gnome                \
		--add-category X-Red-Hat-Base              \
		--add-category Application                 \
		--add-category Utility                     \
		--dir %{buildroot}%{_datadir}/applications \
		%{name}.desktop
%endif

%post
#/sbin/install-info %{_infodir}/*.info.gz %{_infodir}/dir
/sbin/ldconfig 2>/dev/null

%preun
#/sbin/install-info --delete %{_infodir}/*.info.gz %{_infodir}/dir

%postun
/sbin/ldconfig 2>/dev/null

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc AUTHORS ChangeLog COPYING NEWS README TODO
%doc doc/FAQ
%{_bindir}/*
%{_infodir}/cvs*
%{_libdir}/cvs/
%{_mandir}/man?/*
%{_datadir}/gcvs/
%if %{dfi}
        %{_datadir}/gnome/apps/Utilities/*.desktop
%else
        %{_datadir}/applications/*.desktop
%endif

%changelog
* Sun Apr 20 2003 Dag Wieers <dag@wieers.com> - 1.0-0
- Initial package. (using DAR)
