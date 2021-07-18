SOURCE_ARCHIVE := v2.2.6.tar.gz
TARGZ_FILE := h2o.tar.gz
IMAGE_NAME := h2o-package

.PHONY: all
all: amazonlinux2 centos7 centos8 almalinux8 rockylinux8

.PHONY: amazonlinux2
amazonlinux2: amazonlinux2.build

.PHONY: centos7
centos7: centos7.build

.PHONY: centos8
centos8: centos8.build

.PHONY: almalinux8
almalinux8: almalinux8.build

.PHONY: rockylinux8
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

.PHONY: test
test: test-amazonlinux2 test-centos7 test-centos8 test-almalinux8 test-rockylinux8

.PHONY: test-amazonlinux2
test-amazonlinux2:
	./scripts/test.sh amazonlinux2

.PHONY: test-centos7
test-centos7:
	./scripts/test.sh centos7

.PHONY: test-centos8
test-centos8:
	./scripts/test.sh centos8

.PHONY: test-almalinux8
test-almalinux8:
	./scripts/test.sh almalinux8

.PHONY: test-rockylinux8
test-rockylinux8:
	./scripts/test.sh rockylinux8

.PHONY: clean
clean:
	rm -rf *.build.bak *.build bintray
	rm -f rpmbuild/SOURCES/v*.tar.gz
	docker rmi $(IMAGE_NAME)-centos7 || true
	docker rmi $(IMAGE_NAME)-centos8 || true
	docker rmi $(IMAGE_NAME)-almalinux8 || true
	docker rmi $(IMAGE_NAME)-amazonlinux2 || true
	docker rmi $(IMAGE_NAME)-rockylinux8 || true
