#!/bin/sh

set -e

cmake /ext-src/olm -B/tmp/olm-build -DBUILD_SHARED_LIBS=NO -DCMAKE_INSTALL_PREFIX:PATH=/libolm

cmake --build /tmp/olm-build --target install


