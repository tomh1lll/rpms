# $Id$

# Authority: dries
# Upstream: Adam Kennedy <cpan$ali,as>

%define real_name Test-ClassAPI
%define perl_vendorlib %(eval "`perl -V:installvendorlib`"; echo $installvendorlib)
%define perl_vendorarch %(eval "`perl -V:installvendorarch`"; echo $installvendorarch)
%define perl_archlib %(eval "`perl -V:archlib`"; echo $archlib)
%define perl_privlib %(eval "`perl -V:privlib`"; echo $privlib)

Summary: Provides basic first-pass API testing for large class trees
Name: perl-Test-ClassAPI
Version: 1.02
Release: 1
License: Artistic/GPL
Group: Applications/CPAN
URL: http://search.cpan.org/dist/Test-ClassAPI/

Packager: Dries Verachtert <dries@ulyssis.org>
Vendor: Dries Apt/Yum Repository http://dries.ulyssis.org/ayo/

Source: http://search.cpan.org/CPAN/authors/id/A/AD/ADAMK/Test-ClassAPI-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildArch: noarch
BuildRequires: perl

%description
For many APIs with large numbers of classes, it can be very useful to be
able to do a quick once-over to make sure that classes, methods, and
inheritance is correct, before doing more comprehensive testing. This
module aims to provide such a capability.

%prep
%setup -n %{real_name}-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS="vendor" destdir=%{buildroot}
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%makeinstall

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc README Changes
%doc %{_mandir}/man3/*
%{perl_vendorlib}/Test/ClassAPI.pm
%exclude %{perl_archlib}/perllocal.pod
%exclude %{perl_vendorarch}/auto/*/*/.packlist

%changelog
* Sun Jan 16 2005 Dries Verachtert <dries@ulyssis.org> - 1.02-1
- Initial package.

