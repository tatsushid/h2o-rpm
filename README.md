H2O Unofficial RPM package builder
==================================

This provides [H2O](https://h2o.examp1e.net/) RPM spec file and required files
e.g. SysVinit, systemd service etc. to build RPM for Fedora, RHEL/CentOS 6/7
and OpenSUSE.

If you search Debian package, please see [h2o-deb](https://github.com/tatsushid/h2o-deb)

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
- opensuse13
- opensuse-leap

build options.

To build RPM in your server without docker, please copy files under
[`rpmbuild`](https://github.com/tatsushid/h2o-rpm/blob/master/rpmbuild) to your
build system

## Installing RPM

After building, please copy RPM under `*.build` directory to your system and
run

```bash
yum install h2o-2.0.1-2.el6.x86_64.rpm
```

or if you use Fedora 22 or later

```bash
dnf install h2o-2.0.1-2.fc23.x86_64.rpm
```

or if you use OpenSUSE

```bash
zypper install h2o-2.0.1-2.x86_64.rpm
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
[LICENSE](https://github.com/tatsushid/h2o-rpm/blob/master/LICENSE) file for
details.
