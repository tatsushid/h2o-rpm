SOURCE_ARCHIVE := v2.2.6.tar.gz
TARGZ_FILE := h2o.tar.gz
IMAGE_NAME := h2o-package

.PHONY: all clean centos7 centos8 almalinux8 amazonlinux2 rockylinux8

all: centos7 centos8 almalinux8 amazonlinux2 rockylinux8
centos7: centos7.build
centos8: centos8.build
almalinux8: almalinux8.build
amazonlinux2: amazonlinux2.build
rockylinux8: rockylinux8.build

rpmbuild/SOURCES/$(SOURCE_ARCHIVE):
	curl -SL https://github.com/h2o/h2o/archive/$(SOURCE_ARCHIVE) -o rpmbuild/SOURCES/$(SOURCE_ARCHIVE)

%.build: rpmbuild/SPECS/h2o.spec rpmbuild/SOURCES/$(SOURCE_ARCHIVE) \
		rpmbuild/SOURCES/02-fix-c99-compile-error.patch rpmbuild/SOURCES/h2o.conf \
		rpmbuild/SOURCES/h2o.logrotate rpmbuild/SOURCES/h2o.service \
		rpmbuild/SOURCES/h2o.tmpfiles rpmbuild/SOURCES/index.html
	./scripts/build.sh $*

.PHONY: upload
upload:
	./scripts/upload.pl

clean:
	rm -rf *.build.bak *.build bintray tmp Dockerfile
	docker rmi $(IMAGE_NAME)-centos7 || true
	docker rmi $(IMAGE_NAME)-centos8 || true
	docker rmi $(IMAGE_NAME)-almalinux8 || true
	docker rmi $(IMAGE_NAME)-amazonlinux2 || true
	docker rmi $(IMAGE_NAME)-rockylinux8 || true
