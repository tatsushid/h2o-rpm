#!/bin/bash

cd "$(dirname "$0")" || exit 1

TEMPLATE_FILE="bintray.json.tmpl"
DST_DIR="../bintray"
SPEC_FILE="../rpmbuild/SPECS/h2o.spec"

VERSION=$(sed -ne 's/^Version:[[:space:]]*\([.0-9]*\).*/\1/p' "$SPEC_FILE")
RELEASE=$(sed -ne 's/^Release:[[:space:]]*\([.0-9]*\).*/\1/p' "$SPEC_FILE")

PKG_VERSION="${VERSION}-${RELEASE}"
DATE=$(date +%Y-%m-%d)

[ -d "$DST_DIR" ] || mkdir "$DST_DIR"

for PKG_NAME in "$@"; do
    DST_FILE="bintray-${PKG_NAME}.json"

    sed -e "s/@PKG_NAME@/${PKG_NAME}/g" \
        -e "s/@PKG_VERSION@/${PKG_VERSION}/g" \
        -e "s/@DATE@/${DATE}/g" \
        "$TEMPLATE_FILE" > "${DST_DIR}/${DST_FILE}"
done
