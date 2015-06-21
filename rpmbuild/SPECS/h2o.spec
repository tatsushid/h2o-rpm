%define docroot /var/www

%if 0%{?fedora} >= 15 || 0%{?rhel} >= 7
  %global with_systemd 1
%else
  %global with_systemd 0
%endif

#%{?perl_default_filter}
#%global __requires_exclude perl\\(VMS|perl\\(Win32|perl\\(Server::Starter

%{?filter_setup:
%filter_requires_in %{_datadir}
%filter_setup
}

Summary: H2O - The optimized HTTP/1, HTTP/2 server
Name: h2o
Version: 1.3.1
Release: 1%{?dist}
URL: http://h2o.github.io/
Source0: https://github.com/h2o/h2o/archive/v%{version}.tar.gz
Source1: index.html
Source2: h2o.logrotate
Source3: h2o.init
Source4: h2o.service
Source5: h2o.conf
License: MIT
Group: System Environment/Daemons
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: cmake >= 2.8, gcc-c++, openssl-devel, pkgconfig
%if %{with_systemd}
BuildRequires: systemd-units
%endif
Requires: openssl, perl
%if !%{with_systemd}
Requires: initscripts >= 8.36
%endif
%if %{with_systemd}
Requires(preun): systemd-units
Requires(postun): systemd-units
Requires(post): systemd-units
%else
Requires(post): chkconfig
%endif

%description
H2O is a very fast HTTP server written in C. It can also be used
as a library.

%package devel
Group: Development/Libraries
Summary: Development interfaces for H2O
Requires: openssl-devel
Requires: h2o = %{version}-%{release}

%description devel
The h2o-devel package provides H2O library and its header files
which allow you to build your own software using H2O.

%prep
%setup -q

%build
cmake -DWITH_BUNDLED_SSL=on -DCMAKE_INSTALL_PREFIX=%{_prefix} .
make %{?_smp_mflags}

# for building shared library
cmake -DWITH_BUNDLED_SSL=on -DCMAKE_INSTALL_PREFIX=%{_prefix} -DBUILD_SHARED_LIBS=on .
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install

mkdir -p $RPM_BUILD_ROOT/%{_libdir}
install -m 644 -p libh2o-evloop.a \
        $RPM_BUILD_ROOT%{_libdir}/libh2o-evloop.a

%ifarch x86_64
mv $RPM_BUILD_ROOT%{_prefix}/lib/libh2o-evloop.so \
        $RPM_BUILD_ROOT%{_libdir}/libh2o-evloop.so

rm -rf $RPM_BUILD_ROOT%{_prefix}/lib
%endif

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/h2o
install -m 644 -p $RPM_SOURCE_DIR/h2o.conf \
        $RPM_BUILD_ROOT%{_sysconfdir}/h2o/h2o.conf

# docroot
mkdir -p $RPM_BUILD_ROOT%{docroot}/html
install -m 644 -p $RPM_SOURCE_DIR/index.html \
        $RPM_BUILD_ROOT%{docroot}/html/index.html

# Set up /var directories
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/log/h2o

%if %{with_systemd}
# Install systemd service files
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
install -m 644 -p $RPM_SOURCE_DIR/h2o.service \
	$RPM_BUILD_ROOT%{_unitdir}/h2o.service

mkdir -p $RPM_BUILD_ROOT/run/h2o
%else
# install SYSV init stuff
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d
install -m 755 -p $RPM_SOURCE_DIR/h2o.init \
	$RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/h2o

mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/run/h2o
%endif

# install log rotation stuff
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
install -m 644 -p $RPM_SOURCE_DIR/h2o.logrotate \
	$RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/h2o

%define sslcert %{_sysconfdir}/pki/tls/certs/localhost.crt
%define sslkey %{_sysconfdir}/pki/tls/private/localhost.key

%post
%if %{with_systemd}
%systemd_post h2o.service
%else
# Register the h2o service
/sbin/chkconfig --add h2o
%endif

umask 037
if [ -f %{sslkey} -o -f %{sslcert} ]; then
   exit 0
fi

if [ ! -f %{sslkey} ] ; then
%{_bindir}/openssl genrsa -rand /proc/apm:/proc/cpuinfo:/proc/dma:/proc/filesystems:/proc/interrupts:/proc/ioports:/proc/pci:/proc/rtc:/proc/uptime 2048 > %{sslkey} 2> /dev/null
fi

FQDN=`hostname`
if [ "x${FQDN}" = "x" ]; then
   FQDN=localhost.localdomain
fi

if [ ! -f %{sslcert} ] ; then
cat << EOF | %{_bindir}/openssl req -new -key %{sslkey} \
         -x509 -sha256 -days 365 -set_serial $RANDOM -extensions v3_req \
         -out %{sslcert} 2>/dev/null
--
SomeState
SomeCity
SomeOrganization
SomeOrganizationalUnit
${FQDN}
root@${FQDN}
EOF
fi

if [ -f %{sslkey} ]; then
   chgrp nobody %{sslkey}
fi

if [ -f %{sslcert} ]; then
   chgrp nobody %{sslcert}
fi

%preun
%if %{with_systemd}
%systemd_preun h2o.service
%else
if [ $1 = 0 ]; then
	/sbin/service h2o stop > /dev/null 2>&1
	/sbin/chkconfig --del h2o
fi
%endif

%postun
%if %{with_systemd}
%systemd_postun
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)

%dir %{_sysconfdir}/h2o
%config(noreplace) %{_sysconfdir}/h2o/h2o.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/h2o

%if %{with_systemd}
%{_unitdir}/h2o.service
%else
%{_sysconfdir}/rc.d/init.d/h2o
%endif

%{_bindir}/h2o
%{_datadir}/h2o/annotate-backtrace-symbols
%{_datadir}/h2o/fetch-ocsp-response
%{_datadir}/h2o/kill-on-close
%{_datadir}/h2o/start_server

%{_datadir}/doc

%dir %{docroot}
%dir %{docroot}/html
%config(noreplace) %{docroot}/html/index.html

%if %{with_systemd}
%attr(0770,root,nobody) %dir /run/h2o
%else
%attr(0710,root,nobody) %dir %{_localstatedir}/run/h2o
%endif
%attr(0700,root,root) %dir %{_localstatedir}/log/h2o

%files devel
%{_libdir}/libh2o-evloop.a
%{_libdir}/libh2o-evloop.so
%{_includedir}/h2o.h
%{_includedir}/h2o

%changelog
* Sat Jun 20 2015 Tatsushi Demachi <tdemachi@gmail.com> - 1.3.1-1
- update to 1.3.1

* Thu Jun 18 2015 Tatsushi Demachi <tdemachi@gmail.com> - 1.3.0-1
- update to 1.3.0
- move library and headers to devel sub-package

* Fri May 22 2015 Tatsushi Demachi <tdemachi@gmail.com> - 1.2.0-1
- initial package release
