FROM opensuse:42.3
ENV HOME /
RUN zypper -n update
RUN zypper -n install -y rpm-build cmake gcc-c++ tar make openssl-devel ruby ruby-devel bison libuv-devel git
RUN zypper --no-gpg-checks -n -p http://download.opensuse.org/repositories/devel:/tools/openSUSE_Leap_42.3/ install rpmdevtools
RUN rpmdev-setuptree
ADD ./rpmbuild/ /rpmbuild/
RUN chown -R root:root /rpmbuild
RUN rpmbuild -ba /rpmbuild/SPECS/h2o.spec
RUN tar -czf /tmp/h2o.tar.gz -C /rpmbuild RPMS SRPMS
CMD ["/bin/true"]
