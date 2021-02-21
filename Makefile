SOURCE_ARCHIVE := v2.2.6.tar.gz
TARGZ_FILE := h2o.tar.gz
IMAGE_NAME := h2o-package
centos7: IMAGE_NAME := $(IMAGE_NAME)-centos7
centos8: IMAGE_NAME := $(IMAGE_NAME)-centos8
amazonlinux2: IMAGE_NAME := $(IMAGE_NAME)-amazonlinux2

LIBUV_DOWNLOAD_NAME := v1.28.0.tar.gz
LIBUV_ARCHIVE := libuv-$(LIBUV_DOWNLOAD_NAME)

.PHONY: all clean centos6 centos7 fedora opensuse-leap

all: centos7 centos8 amazonlinux2
centos7: centos7.build
centos8: centos8.build
amazonlinux2: amazonlinux2.build

rpmbuild/SOURCES/$(SOURCE_ARCHIVE):
	curl -SL https://github.com/h2o/h2o/archive/$(SOURCE_ARCHIVE) -o rpmbuild/SOURCES/$(SOURCE_ARCHIVE)

deps/$(LIBUV_ARCHIVE):
	[ -d deps ] || mkdir deps
	curl -SL https://github.com/libuv/libuv/archive/$(LIBUV_DOWNLOAD_NAME) -o deps/$(LIBUV_ARCHIVE)

%.build: deps/$(LIBUV_ARCHIVE) rpmbuild/SPECS/h2o.spec rpmbuild/SOURCES/$(SOURCE_ARCHIVE)
	[ -d $@.bak ] && rm -rf $@.bak || :
	[ -d $@ ] && mv $@ $@.bak || :
	tar -czf - Dockerfile.$* rpmbuild deps | docker build --file Dockerfile.$* -t $(IMAGE_NAME) -
	docker run --name $(IMAGE_NAME)-tmp $(IMAGE_NAME)
	mkdir -p tmp
	docker wait $(IMAGE_NAME)-tmp
	docker cp $(IMAGE_NAME)-tmp:/tmp/$(TARGZ_FILE) tmp
	docker rm $(IMAGE_NAME)-tmp
	mkdir $@
	tar -xzf tmp/$(TARGZ_FILE) -C $@
	rm -rf tmp Dockerfile
	docker images | grep -q $(IMAGE_NAME) && docker rmi $(IMAGE_NAME) || true

bintray:
	./scripts/build_bintray_json.bash \
		h2o \
		h2o-debuginfo \
		libh2o \
		libh2o-evloop \
		libh2o-devel

clean:
	rm -rf *.build.bak *.build bintray tmp Dockerfile
	docker rmi $(IMAGE_NAME)-centos7 || true
	docker rmi $(IMAGE_NAME)-centos8 || true
	docker rmi $(IMAGE_NAME)-amazonlinux2 || true
