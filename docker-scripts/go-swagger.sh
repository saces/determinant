#!/bin/sh

#set -e

mkdir -p /go/src/determinant/push/

/go/bin/swagger generate client -f /matrix-spec/determinant/push-gateway.swagger.yaml -t /go/src/determinant/push/

mkdir -p /go/src/determinant/is/

/go/bin/swagger generate client -f /matrix-spec/determinant/identity.swagger.yaml -t /go/src/determinant/is/

mkdir -p /go/src/determinant/as/

/go/bin/swagger generate client -f /matrix-spec/determinant/application-service.swagger.yaml -t /go/src/determinant/as/

mkdir -p /go/src/determinant/ss/

/go/bin/swagger generate client -f /matrix-spec/determinant/server-server.swagger.yaml -t /go/src/determinant/ss/

mkdir -p /go/src/determinant/cs/

/go/bin/swagger generate client -f /matrix-spec/determinant/client-server.swagger.yaml -t /go/src/determinant/cs/
