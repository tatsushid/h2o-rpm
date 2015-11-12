SOURCE_ARCHIVE := v1.5.4.tar.gz
TARGZ_FILE := h2o.tar.gz
IMAGE_NAME := h2o-package
centos6: IMAGE_NAME := $(IMAGE_NAME)-ce6
centos7: IMAGE_NAME := $(IMAGE_NAME)-ce7
fedora: IMAGE_NAME := $(IMAGE_NAME)-fc23
opensuse: IMAGE_NAME := $(IMAGE_NAME)-suse13.2

.PHONY: all clean centos6 centos7 fedora opensuse

all: centos6 centos7 fedora opensuse
centos6: centos6.build
centos7: centos7.build
fedora: fedora.build
opensuse: opensuse.build

rpmbuild/SOURCES/$(SOURCE_ARCHIVE):
	curl -SL https://github.com/h2o/h2o/archive/$(SOURCE_ARCHIVE) -o rpmbuild/SOURCES/$(SOURCE_ARCHIVE)

%.build: rpmbuild/SPECS/h2o.spec rpmbuild/SOURCES/$(SOURCE_ARCHIVE)
	[ -d $@.bak ] && rm -rf $@.bak || :
	[ -d $@ ] && mv $@ $@.bak || :
	cp Dockerfile.$* Dockerfile
	tar -czf - Dockerfile rpmbuild | docker build -t $(IMAGE_NAME) -
	docker run --name $(IMAGE_NAME)-tmp $(IMAGE_NAME)
	mkdir -p tmp
	docker wait $(IMAGE_NAME)-tmp
	docker cp $(IMAGE_NAME)-tmp:/tmp/$(TARGZ_FILE) tmp
	docker rm $(IMAGE_NAME)-tmp
	mkdir $@
	tar -xzf tmp/$(TARGZ_FILE) -C $@
	rm -rf tmp Dockerfile
	docker images | grep -q $(IMAGE_NAME) && docker rmi $(IMAGE_NAME) || true

clean:
	rm -rf *.build.bak *.build tmp Dockerfile
	docker images | grep -q $(IMAGE_NAME)-ce6 && docker rmi $(IMAGE_NAME)-ce6 || true
	docker images | grep -q $(IMAGE_NAME)-ce7 && docker rmi $(IMAGE_NAME)-ce7 || true
	docker images | grep -q $(IMAGE_NAME)-fc23 && docker rmi $(IMAGE_NAME)-fc23 || true
	docker images | grep -q $(IMAGE_NAME)-suse13.2 && docker rmi $(IMAGE_NAME)-suse13.2 || true
