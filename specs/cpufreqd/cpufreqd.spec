# Authority: dag

Summary: CPU frequency scaling daemon.
Name: cpufreqd
Version: 1.1.1
Release: 0
License: GPL
Group: System Environment/Kernel
URL: http://sourceforge.net/projects/cpufreqd/

Packager: Dag Wieers <dag@wieers.com>
Vendor: Dag Apt Repository, http://dag.wieers.com/apt/

Source: http://dl.sf.net/cpufreqd/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/root-%{name}-%{version}
Prefix: %{_prefix}

%description
cpufreqd is meant to be a replacement of the speedstep applet you
can find on some other OS, it monitors battery level, AC state and
running programs and adjusts the frequency of the processor according to
a set of rules specified in the config file (see cpufreqd.conf (5)).

%prep
%setup

### Put default to apm instead of acpi
%{__perl} -pi.orig -e 's|^(pm_type=.*)$|#$1\npm_type=apm|' cpufreqd.conf

%{__cat} <<EOF >cpufreqd.sysconfig
SPEEDSTEP_MODULE="speedstep-centrino"
#SPEEDSTEP_MODULE="speedstep-ich"
EOF

%{__cat} <<'EOF' >cpufreqd.sysv
#!/bin/bash
#
# Init file for cpufreqd.
#
# Written by Dag Wieers <dag@wieers.com>.
#
# chkconfig: 2345 05 95
# description: CPU frequency scaling daemon.
#
# processname: cpufreqd
# config: %{_sysconfdir}/sysconfig/cpufreqd
# pidfile: /var/run/arpd.pid

source %{_initrddir}/functions

### Default variables
SPEEDSTEP_MODULE="speedstep-centrino"

[ -x %{_sbindir}/cpufreqd ] || exit 1
[ -r %{_sysconfdir}/sysconfig/cpufreqd ] && source %{_sysconfdir}/sysconfig/cpufreqd

RETVAL=0
prog="cpufreqd" 
desc="CPU frequency scaling deamon"

start() {
	if [ $SPEEDSTEP_MODULE ]; then
		/sbin/modprobe -k $SPEEDSTEP_MODULE
	fi
	echo -n $"Starting $desc ($prog): "
	daemon $prog
	RETVAL=$?
	echo
	[ $RETVAL -eq 0 ] && touch %{_localstatedir}/lock/subsys/$prog
	return $RETVAL
}

stop() {
        echo -n $"Shutting down $desc ($prog): "
        killproc $prog
        RETVAL=$?
        echo
        [ $RETVAL -eq 0 ] && rm -f %{_localstatedir}/lock/subsys/$prog
        return $RETVAL
}

restart() {
	stop
	start
}

case "$1" in
  start)
	start
	;;
  stop)
	stop
	;;
  restart|reload)
	restart
	;;
  condrestart)
	[ -e %{_localstatedir}/lock/subsys/$prog ] && restart
	RETVAL=$?
	;;
  status)
	status $prog
	RETVAL=$?
	;;
  *)
	echo $"Usage: $0 {start|stop|restart|condrestart|status}"
	RETVAL=1
esac

exit $RETVAL
EOF

%build
%configure \
	--program-prefix="%{?_program_prefix}"
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%makeinstall
%{__install} -d -m0755 %{buildroot}%{_sysconfdir}/sysconfig/ \
			%{buildroot}%{_initrddir}
%{__install} -m0755 cpufreqd.sysv %{buildroot}%{_initrddir}/cpufreqd
%{__install} -m0644 cpufreqd.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/cpufreqd

%clean
%{__rm} -rf %{buildroot}

%post
/sbin/chkconfig --add cpufreqd

%preun
if [ $1 -eq 0 ]; then
 /sbin/service cpufreqd stop &>/dev/null || :
 /sbin/chkconfig --del cpufreqd
fi

%postun
/sbin/service cpufreqd condrestart &>/dev/null || :

%files
%defattr(-, root, root, 0755)
%doc AUTHORS COPYING README TODO
%doc %{_mandir}/man?/*
%config(noreplace) %{_sysconfdir}/cpufreqd.conf
%config(noreplace) %{_sysconfdir}/sysconfig/*
%config %{_initrddir}/*
%{_sbindir}/*
%{_libdir}/*

%changelog
* Mon Feb 09 2004 Dag Wieers <dag@wieers.com> - 1.1.1-0
- Updated to release 1.1.1.

* Tue Jan 20 2004 Dag Wieers <dag@wieers.com> - 1.1-2
- Fixed sysv script to use %%{_sbindir}. (Stefanos Zachariadis)

* Tue Jan 06 2004 Dag Wieers <dag@wieers.com> - 1.1-1
- Updated to release 1.1.

* Mon Dec 01 2003 Dag Wieers <dag@wieers.com> - 1.1-0.rc1
- Initial package. (using DAR)
