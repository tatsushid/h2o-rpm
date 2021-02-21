#!/bin/bash

set -exu

ROOT=$(cd "$(dirname "$0")/../" && pwd)

DISTRO=$1
: "${PLATFORM:=linux/amd64}"
IMAGE_NAME=h2o-package-$DISTRO
TARGZ_FILE=h2o.tar.gz

rm -rf "$DISTRO.build.bak"
if [[ -d "$DISTRO.build" ]];
then
    mv "$DISTRO.build" "$DISTRO.build.bak"
fi

docker buildx build \
    --load \
    --platform "$PLATFORM" \
    --file "Dockerfile.$DISTRO" \
    -t "$IMAGE_NAME" "$ROOT"

docker run --platform "$PLATFORM" --name "$IMAGE_NAME-tmp" "$IMAGE_NAME"
mkdir -p "$ROOT/tmp"
docker wait "$IMAGE_NAME-tmp"
	docker cp "$IMAGE_NAME-tmp:/tmp/$TARGZ_FILE" "$ROOT/tmp"
docker rm "$IMAGE_NAME-tmp"

mkdir -p "$DISTRO.build"
tar -xzf "$ROOT/tmp/$TARGZ_FILE" -C "$DISTRO.build"
rm -rf "$ROOT/tmp"
