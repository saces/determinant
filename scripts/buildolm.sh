#!/bin/sh

set -e

cmake /ext-src/olm -B/olm-build -DBUILD_SHARED_LIBS=NO -DCMAKE_INSTALL_PREFIX:PATH=/libolm

cmake --build /olm-build --target install


