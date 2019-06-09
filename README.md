H2O Unofficial RPM package builder
==================================

[![Build Status](https://travis-ci.com/shogo82148/h2o-rpm.svg?branch=master)](https://travis-ci.com/shogo82148/h2o-rpm)

This provides [H2O](https://h2o.examp1e.net/) RPM spec file and required files
e.g. SysVinit, systemd service etc. to build RPM for Fedora, RHEL/CentOS 6/7,
OpenSUSE and Amazon Linux 2.

If you search Debian package, please see [h2o-deb](https://github.com/shogo82148/h2o-deb)

## How to use prebuilt RPM

This has [Bintray RPM repository](https://bintray.com/shogo82148/h2o-rpm) so if
you'd like to just install such a prebuilt package, please put following into a
`bintray-shogo82148-h2o-rpm.repo` in `/etc/yum.repos.d`

CentOS:

```ini
#bintray-shogo82148-h2o-rpm - packages by shogo82148 from Bintray
[bintray-shogo82148-h2o-rpm]
name=bintray-shogo82148-h2o-rpm
#If your system is CentOS
baseurl=https://dl.bintray.com/shogo82148/h2o-rpm/centos/$releasever/$basearch/
gpgcheck=0
repo_gpgcheck=1
enabled=1
gpgkey=https://bintray.com/api/v1/usrs/shogo82148/keys/gpg/public.key
```

Fedora:

```ini
#bintray-shogo82148-h2o-rpm - packages by shogo82148 from Bintray
[bintray-shogo82148-h2o-rpm]
name=bintray-shogo82148-h2o-rpm
baseurl=https://dl.bintray.com/shogo82148/h2o-rpm/fedora/$releasever/$basearch/
gpgcheck=0
repo_gpgcheck=1
enabled=1
gpgkey=https://bintray.com/api/v1/usrs/shogo82148/keys/gpg/public.key
```

Amazon Linux 2:

```ini
#bintray-shogo82148-h2o-rpm - packages by shogo82148 from Bintray
[bintray-shogo82148-h2o-rpm]
name=bintray-shogo82148-h2o-rpm
baseurl=https://dl.bintray.com/shogo82148/h2o-rpm/amazonlinux2/$releasever/$basearch/
gpgcheck=0
repo_gpgcheck=1
enabled=1
gpgkey=https://bintray.com/api/v1/usrs/shogo82148/keys/gpg/public.key
```

Once the file is correctly saved, you can install packages in the repository by

```bash
yum install h2o
```

or if you use Fedora

```bash
dnf install h2o
```

## How to build RPM

If you have a docker environment, you can build RPMs by just running

```bash
make
```

If you'd like to build RPM for specific distribution, please run a command like
following

```bash
make centos6
```

Now this understands

- centos6
- centos7
- fedora
- opensuse-leap
- amazonlinux2

build options.

To build RPM in your server without docker, please copy files under
[`rpmbuild`](https://github.com/shogo82148/h2o-rpm/blob/master/rpmbuild) to your
build system

## Installing RPM

After building, please copy RPM under `*.build` directory to your system and
run

```bash
yum install h2o-2.2.5-1.el6.x86_64.rpm
```

or if you use Fedora 22 or later

```bash
dnf install h2o-2.2.5-1.fc29.x86_64.rpm
```

or if you use OpenSUSE

```bash
zypper install h2o-2.2.5-1.x86_64.rpm
```

Once the installation finishes successfully, you can see a configuration file
at `/etc/h2o/h2o.conf`.

To start h2o, please run

```bash
service h2o start
```

or

```bash
systemctl enable h2o.service
systemctl start h2o.service
```

## License

This is under MIT License. Please see the
[LICENSE](https://github.com/shogo82148/h2o-rpm/blob/master/LICENSE) file for
details.
