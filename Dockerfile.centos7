FROM centos:7
ENV HOME /
RUN yum update -y
RUN yum install -y epel-release
RUN yum install -y rpm-build redhat-rpm-config rpmdevtools cmake gcc-c++ tar make openssl-devel ruby ruby-devel bison automake libtool libuv-devel git
RUN rpmdev-setuptree
RUN echo '%dist   .el7' >> /.rpmmacros
ADD ./rpmbuild/ /rpmbuild/
RUN chown -R root:root /rpmbuild
RUN rpmbuild -ba /rpmbuild/SPECS/h2o.spec
RUN tar -czf /tmp/h2o.tar.gz -C /rpmbuild RPMS SRPMS
CMD ["/bin/true"]
