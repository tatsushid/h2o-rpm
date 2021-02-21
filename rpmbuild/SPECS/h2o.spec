%define docroot /var/www

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
Version: 2.2.6
Release: 1%{?dist}
URL: https://h2o.examp1e.net/
Source0: https://github.com/h2o/h2o/archive/v%{version}.tar.gz
Source1: index.html
Source2: h2o.logrotate
Source4: h2o.service
Source5: h2o.conf
Patch1: 02-fix-c99-compile-error.patch
License: MIT
Group: System Environment/Daemons
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: cmake >= 2.8, gcc-c++, openssl-devel, pkgconfig
%if 0%{?rhel} == 6
BuildRequires: rh-ruby24-ruby-devel, bison
%else
BuildRequires: ruby-devel >= 1.9, bison
%endif
Requires: openssl, perl
BuildRequires: systemd-units
Requires(preun): systemd
Requires(postun): systemd
Requires(post): systemd

%description
H2O is a very fast HTTP server written in C

%package -n libh2o
Group: Development/Libraries
Summary: H2O Library compiled with libuv

%description -n libh2o
libh2o package provides H2O library compiled with libuv which allows you to
link your own software to H2O.

%package -n libh2o-evloop
Group: Development/Libraries
Summary: H2O Library compiled with its own event loop

%description -n libh2o-evloop
libh2o-evloop package provides H2O library compiled with its own event loop
which allows you to link your own software to H2O.

%package -n libh2o-devel
Group: Development/Libraries
Summary: Development interfaces for H2O
Requires: openssl-devel, pkgconfig
Requires: libh2o = %{version}-%{release}
Requires: libh2o-evloop = %{version}-%{release}
Obsoletes: h2o-devel

%description -n libh2o-devel
libh2o-devel package provides H2O header files and helpers which allow you to
build your own software using H2O.

%prep
%setup -q
%patch1 -p1 -b .c99

%build
cmake -DWITH_BUNDLED_SSL=on -DWITH_MRUBY=on -DCMAKE_INSTALL_PREFIX=%{_prefix} -DBUILD_SHARED_LIBS=on .
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install

mv $RPM_BUILD_ROOT%{_prefix}/bin \
        $RPM_BUILD_ROOT%{_sbindir}

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/h2o
install -m 644 -p $RPM_SOURCE_DIR/h2o.conf \
        $RPM_BUILD_ROOT%{_sysconfdir}/h2o/h2o.conf


# Set up /var directories
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/log/h2o

# Install systemd service files
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
install -m 644 -p $RPM_SOURCE_DIR/h2o.service \
	$RPM_BUILD_ROOT%{_unitdir}/h2o.service

mkdir -p $RPM_BUILD_ROOT/run/h2o

# Install tmpfiles.d configuration
mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/tmpfiles.d
install -m 644 -p $RPM_SOURCE_DIR/h2o.tmpfiles \
	$RPM_BUILD_ROOT%{_prefix}/lib/tmpfiles.d/h2o.conf

# install log rotation stuff
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
install -m 644 -p $RPM_SOURCE_DIR/h2o.logrotate \
	$RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/h2o

%define sslcert %{_sysconfdir}/pki/tls/certs/localhost.crt
%define sslkey %{_sysconfdir}/pki/tls/private/localhost.key

%pre

%post
%systemd_post h2o.service


%preun
%systemd_preun h2o.service

%postun
%systemd_postun

%post -n libh2o -p /sbin/ldconfig

%postun -n libh2o -p /sbin/ldconfig

%post -n libh2o-evloop -p /sbin/ldconfig

%postun -n libh2o-evloop -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)

%dir %{_sysconfdir}/h2o
%config(noreplace) %{_sysconfdir}/h2o/h2o.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/h2o

%{_unitdir}/h2o.service

%{_prefix}/lib/tmpfiles.d/h2o.conf

%{_sbindir}/h2o
%{_datadir}/h2o/annotate-backtrace-symbols
%{_datadir}/h2o/fastcgi-cgi
%{_datadir}/h2o/fetch-ocsp-response
%{_datadir}/h2o/kill-on-close
%{_datadir}/h2o/setuidgid
%{_datadir}/h2o/start_server

%{_datadir}/h2o/mruby
%{_datadir}/doc

%{_datadir}/h2o/ca-bundle.crt
%{_datadir}/h2o/status

%attr(0770,root,nobody) %dir /run/h2o
%attr(0700,root,root) %dir %{_localstatedir}/log/h2o

%files -n libh2o
%{_libdir}/libh2o.so.*

%files -n libh2o-evloop
%{_libdir}/libh2o-evloop.so.*

%files -n libh2o-devel
%{_libdir}/libh2o.so
%{_libdir}/libh2o-evloop.so
%{_libdir}/pkgconfig/libh2o.pc
%{_libdir}/pkgconfig/libh2o-evloop.pc
%{_includedir}/h2o.h
%{_includedir}/h2o

%changelog
* Wed Aug 14 2019 Ichinose Shogo <shogo82148@gmail.com> - 2.2.6-1
- This is a bug-fix release of the 2.2 series with following changes from 2.2.5, including a vulnerability fix.
- [security fix][http2] fix HTTP/2 DoS attack vectors CVE-2019-9512 CVE-2019-9514 CVE-2019-9515 #2090 (Kazuho Oku)

* Wed May  1 2019 Ichinose Shogo <shogo82148@gmail.com> - 2.2.5-2
- Add amazonlinux2 support

* Fri Jun  1 2018 Tatsushi Demachi <tdemachi@gmail.com> - 2.2.5-1
- Update to 2.2.5
- Add patch for avoid c99 syntax issue at compilation

* Fri Dec 15 2017 Tatsushi Demachi <tdemachi@gmail.com> - 2.2.4-1
- Update to 2.2.4
- Remove patch for fixing mruby behavior because it has been fixed by upstream
  in this version

* Thu Oct 19 2017 Tatsushi Demachi <tdemachi@gmail.com> - 2.2.3-1
- Update to 2.2.3
- Add patch for fixing mruby behavior on 2.2.3

* Sat Apr 29 2017 Tatsushi Demachi <tdemachi@gmail.com> - 2.2.2-1
- Update to 2.2.2

* Sat Apr 29 2017 Tatsushi Demachi <tdemachi@gmail.com> - 2.2.0-2
- Add libuv-devel build dependency to libh2o

* Thu Apr  6 2017 Tatsushi Demachi <tdemachi@gmail.com> - 2.2.0-1
- Update to 2.2.0

* Wed Jan 18 2017 Tatsushi Demachi <tdemachi@gmail.com> - 2.1.0-1
- Update to 2.1.0

* Wed Dec 21 2016 Tatsushi Demachi <tdemachi@gmail.com> - 2.0.5-1
- Update to 2.0.5

* Wed Sep 14 2016 Tatsushi Demachi <tdemachi@gmail.com> - 2.0.4-1
- Update to 2.0.4

* Thu Sep  8 2016 Tatsushi Demachi <tdemachi@gmail.com> - 2.0.3-1
- Update to 2.0.3

* Tue Aug 23 2016 Tatsushi Demachi <tdemachi@gmail.com> - 2.0.2-1
- Update to 2.0.2

* Wed Jul 27 2016 Tatsushi Demachi <tdemachi@gmail.com> - 2.0.1-2
- Remove openssl package dependency from libh2o and libh2o-evloop packages
- Put h2o binary in /usr/sbin directory instead of /usr/bin directory

* Sat Jun 25 2016 Tatsushi Demachi <tdemachi@gmail.com> - 2.0.1-1
- Update to 2.0.1
- Remove patches by upstream fix

* Sat Jun  4 2016 Tatsushi Demachi <tdemachi@gmail.com> - 2.0.0-1
- Update to 2.0.0
- Add patch to avoid c++ header issue caused by libuv 1.4.2 or earlier

* Sat Jun  4 2016 Tatsushi Demachi <tdemachi@gmail.com> - 1.7.3-2
- Rename and split h2o-devel package in libh2o, libh2o-evloop and libh2o-devel
- Stop providing static libraries.
- Fix broken library links
- Fix wrong pkg-config's library paths in x86_64 environment

* Sat May 28 2016 Tatsushi Demachi <tdemachi@gmail.com> - 1.7.3-1
- Update to 1.7.3
- Add tmpfiles.d configuration to fix the issue that PID file's parent
  directory is removed after restarting system
- Change 'ruby' build requires to 'ruby-devel'

* Mon May  9 2016 Tatsushi Demachi <tdemachi@gmail.com> - 1.7.2-1
- Update to 1.7.2

* Mon Mar 14 2016 Tatsushi Demachi <tdemachi@gmail.com> - 1.7.1-1
- Update to 1.7.1
- Add pkgconfig dependency to devel sub package

* Fri Feb  5 2016 Tatsushi Demachi <tdemachi@gmail.com> - 1.7.0-1
- Update to 1.7.0

* Fri Feb  5 2016 Tatsushi Demachi <tdemachi@gmail.com> - 1.6.3-1
- Update to 1.6.3

* Wed Jan 13 2016 Tatsushi Demachi <tdemachi@gmail.com> - 1.6.2-1
- Update to 1.6.2

* Sat Dec 19 2015 Tatsushi Demachi <tdemachi@gmail.com> - 1.6.1-1
- Update to 1.6.1

* Sat Dec  5 2015 Tatsushi Demachi <tdemachi@gmail.com> - 1.6.0-1
- Update to 1.6.0
- Remove patch by upstream fix

* Thu Nov 12 2015 Tatsushi Demachi <tdemachi@gmail.com> - 1.5.4-1
- Update to 1.5.4

* Sat Nov  7 2015 Tatsushi Demachi <tdemachi@gmail.com> - 1.5.3-1
- Update to 1.5.3

* Mon Nov  2 2015 Tatsushi Demachi <tdemachi@gmail.com> - 1.5.2-2
- Add mruby support
- Fix official URL

* Tue Oct 20 2015 Tatsushi Demachi <tdemachi@gmail.com> - 1.5.2-1
- Update to 1.5.2

* Fri Oct  9 2015 Tatsushi Demachi <tdemachi@gmail.com> - 1.5.0-2
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
