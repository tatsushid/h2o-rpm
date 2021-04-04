# H2O Unofficial RPM package builder

[![build](https://github.com/shogo82148/h2o-rpm/actions/workflows/build.yml/badge.svg)](https://github.com/shogo82148/h2o-rpm/actions/workflows/build.yml)

This provides [H2O](https://h2o.examp1e.net/) RPM spec file and required files
e.g. systemd service etc. to build RPM for RHEL/CentOS 7/8, and Amazon Linux 2.

## How to use prebuilt RPM

Once the file is correctly saved, you can install packages in the repository by

```bash
yum install h2o
```

### Amazon Linux 2

To add unofficial h2o yum repository, create a file named `/etc/yum.repos.d/shogo82148.repo`.

```ini
# shogo82148-rpm - packages by shogo82148
[shogo82148-rpm]
name=shogo82148-rpm
baseurl=https://shogo82148-rpm-repository.s3-ap-northeast-1.amazonaws.com/amazonlinux/$releasever/$basearch/
gpgcheck=1
enabled=1
gpgkey=https://shogo82148-rpm-repository.s3-ap-northeast-1.amazonaws.com/RPM-GPG-KEY-shogo82148
```

Or install the RPM package for configure the repository.

```
yum install -y https://shogo82148-rpm-repository.s3-ap-northeast-1.amazonaws.com/amazonlinux/2/noarch/shogo82148/shogo82148-1.0.0-1.amzn2.noarch.rpm
```

### CentOS 7 and 8

To add unofficial h2o yum repository, create a file named `/etc/yum.repos.d/shogo82148.repo`.

```ini
# shogo82148-rpm - packages by shogo82148
[shogo82148-rpm]
name=shogo82148-rpm
baseurl=https://shogo82148-rpm-repository.s3-ap-northeast-1.amazonaws.com/centos/$releasever/$basearch/
gpgcheck=1
enabled=1
gpgkey=https://shogo82148-rpm-repository.s3-ap-northeast-1.amazonaws.com/RPM-GPG-KEY-shogo82148
```

Or install the RPM package for configure the repository.

```bash
# CentOS 7
yum install -y https://shogo82148-rpm-repository.s3-ap-northeast-1.amazonaws.com/centos/7/noarch/shogo82148/shogo82148-1.0.0-1.el7.noarch.rpm

# CentOS 8
dnf install -y https://shogo82148-rpm-repository.s3-ap-northeast-1.amazonaws.com/centos/8/noarch/shogo82148/shogo82148-1.0.0-1.el8.noarch.rpm
```

## License

This is under MIT License. Please see the
[LICENSE](https://github.com/shogo82148/h2o-rpm/blob/master/LICENSE) file for
details.
