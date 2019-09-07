package main

import "testing"

func TestTransposer(t *testing.T) {
	root := "../ext-src/matrix-doc"
	//transpose(root, "application-service")
	//transpose(root, "client-server")x
	//transpose(root, "identity")
	transpose(root, "push-gateway")
	//transpose(root, "server-server")
}
