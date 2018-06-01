FROM fedora:28
ENV HOME /
RUN dnf update -y
RUN dnf install -y rpm-build redhat-rpm-config rpmdevtools cmake gcc-c++ tar make openssl-devel ruby ruby-devel bison libuv-devel git
RUN rpmdev-setuptree
RUN echo '%dist   .fc28' >> /.rpmmacros
ADD ./rpmbuild/ /rpmbuild/
RUN chown -R root:root /rpmbuild
RUN rpmbuild -ba /rpmbuild/SPECS/h2o.spec
RUN tar -czf /tmp/h2o.tar.gz -C /rpmbuild RPMS SRPMS
CMD ["/bin/true"]
