#!/bin/sh

set -e

docker-compose build olm-src
docker-compose run -u $(id -u ${USER}):$(id -g ${USER}) olm-src

docker-compose build olm-lib
docker-compose run -u $(id -u ${USER}):$(id -g ${USER}) olm-lib
