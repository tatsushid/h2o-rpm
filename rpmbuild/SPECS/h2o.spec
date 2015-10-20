%define docroot /var/www

%if 0%{?fedora} >= 15 || 0%{?rhel} >= 7 || 0%{?suse_version} >= 1210
  %global with_systemd 1
%else
  %global with_systemd 0
%endif

%if 0%{?fedora} >= 15 || 0%{?rhel} >= 7
%{?perl_default_filter}
%global __requires_exclude perl\\(VMS|perl\\(Win32|perl\\(Server::Starter
%else
%if 0%{?rhel} == 6
%{?filter_setup:
%filter_requires_in %{_datadir}
%filter_setup
}
%endif
%endif

Summary: H2O - The optimized HTTP/1, HTTP/2 server
Name: h2o
Version: 1.5.2
Release: 1%{?dist}
URL: http://h2o.github.io/
Source0: https://github.com/h2o/h2o/archive/v%{version}.tar.gz
Source1: index.html
Source2: h2o.logrotate
Source3: h2o.init
Source4: h2o.service
Source5: h2o.conf
Patch1: h2o-cmake-version.patch
License: MIT
Group: System Environment/Daemons
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: cmake >= 2.8, gcc-c++, openssl-devel, pkgconfig
Requires: openssl, perl
%if %{with_systemd}
%if 0%{?suse_version}
BuildRequires: systemd-rpm-macros
%{?systemd_requires}
%else
BuildRequires: systemd-units
Requires(preun): systemd
Requires(postun): systemd
Requires(post): systemd
%endif
%else
Requires: initscripts >= 8.36
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
%patch1 -p1 -b .cmakeversion

%build
cmake -DWITH_BUNDLED_SSL=on -DCMAKE_INSTALL_PREFIX=%{_prefix} .
make %{?_smp_mflags}

# for building shared library
cmake -DWITH_BUNDLED_SSL=on -DCMAKE_INSTALL_PREFIX=%{_prefix} -DBUILD_SHARED_LIBS=on .
make %{?_smp_mflags}

%if !%{with_systemd}
sed -i -e 's,\( *\).*systemctl.* >,\1/sbin/service h2o reload >,' %{SOURCE2}
%endif

%if 0%{?suse_version}
sed -i -e '/localhost:443/,/file.dir/s/^/#/' -e 's|\(file.dir: \).*|\1/srv/www/htdocs|' %{SOURCE5}
%endif

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

%if 0%{?suse_version} == 0
# docroot
mkdir -p $RPM_BUILD_ROOT%{docroot}/html
install -m 644 -p $RPM_SOURCE_DIR/index.html \
        $RPM_BUILD_ROOT%{docroot}/html/index.html
%endif

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

%pre
%if %{with_systemd} && 0%{?suse_version}
%service_add_pre h2o.service
%endif

%post
%if %{with_systemd}
%if 0%{?suse_version}
%service_add_post h2o.service
%else
%systemd_post h2o.service
%endif
%else
# Register the h2o service
/sbin/chkconfig --add h2o
%endif

%if 0%{?suse_version} == 0
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
%endif

%preun
%if %{with_systemd}
%if 0%{?suse_version}
%service_del_preun h2o.service
%else
%systemd_preun h2o.service
%endif
%else
if [ $1 = 0 ]; then
	/sbin/service h2o stop > /dev/null 2>&1
	/sbin/chkconfig --del h2o
fi
%endif

%postun
%if %{with_systemd}
%if 0%{?suse_version}
%service_del_postun h2o.service
%else
%systemd_postun
%endif
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
%{_datadir}/h2o/setuidgid
%{_datadir}/h2o/start_server

%{_datadir}/doc

%if 0%{?suse_version} == 0
%dir %{docroot}
%dir %{docroot}/html
%config(noreplace) %{docroot}/html/index.html
%endif

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
* Tue Oct 20 2015 Tatsushi Demachi <tdemachi@gmail.com> - 1.5.2-1
- Update to 1.5.2

* Wed Oct  9 2015 Tatsushi Demachi <tdemachi@gmail.com> - 1.5.0-2
- Add patch to fix CMake version issue for CentOS 7 build

* Thu Oct  8 2015 Donald Stufft <donald@stufft.io> - 1.5.0-1
- Update to 1.5.0

* Wed Sep 16 2015 Tatsushi Demachi <tdemachi@gmail.com> - 1.4.5-1
- Update to 1.4.5

* Tue Aug 18 2015 Tatsushi Demachi <tdemachi@gmail.com> - 1.4.4-1
- Update to 1.4.4

* Mon Aug 17 2015 Tatsushi Demachi <tdemachi@gmail.com> - 1.4.3-1
- Update to 1.4.3

* Wed Jul 29 2015 Tatsushi Demachi <tdemachi@gmail.com> - 1.4.2-1
- Update to 1.4.2

* Thu Jul 23 2015 Tatsushi Demachi <tdemachi@gmail.com> - 1.4.1-1
- Update to 1.4.1

* Tue Jun 23 2015 Tatsushi Demachi <tdemachi@gmail.com> - 1.3.1-4
- Add OpenSUSE support

* Mon Jun 22 2015 Tatsushi Demachi <tdemachi@gmail.com> - 1.3.1-3
- Fix logrotate

* Sun Jun 21 2015 Tatsushi Demachi <tdemachi@gmail.com> - 1.3.1-2
- Add fedora support

* Sat Jun 20 2015 Tatsushi Demachi <tdemachi@gmail.com> - 1.3.1-1
- Update to 1.3.1

* Thu Jun 18 2015 Tatsushi Demachi <tdemachi@gmail.com> - 1.3.0-1
- Update to 1.3.0
- Move library and headers to devel sub-package

* Fri May 22 2015 Tatsushi Demachi <tdemachi@gmail.com> - 1.2.0-1
- Initial package release
