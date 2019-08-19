#!/bin/sh

set -e

docker-compose build olm-src
docker-compose run -u $(id -u ${USER}):$(id -g ${USER}) olm-src

docker-compose build olm-lib
docker-compose run -u $(id -u ${USER}):$(id -g ${USER}) olm-lib

docker-compose build go-olm-src
docker-compose run -u $(id -u ${USER}):$(id -g ${USER}) go-olm-src

docker-compose build matrix-doc-src
docker-compose run -u $(id -u ${USER}):$(id -g ${USER}) matrix-doc-src

docker-compose build matrix-doc-gen
docker-compose run -u $(id -u ${USER}):$(id -g ${USER}) matrix-doc-gen

docker-compose build generate-client-api
docker-compose run -u $(id -u ${USER}):$(id -g ${USER}) generate-client-api
