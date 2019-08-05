#!/bin/sh

set -e

docker-compose build olm-src
docker-compose run olm-src

docker-compose build olm-lib
docker-compose run olm-lib
