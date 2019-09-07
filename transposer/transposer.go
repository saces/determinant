package main

import (
	"io/ioutil"
	"log"
	"os"
	"path"
	"strings"

	"github.com/getkin/kin-openapi/openapi2conv"

	"github.com/getkin/kin-openapi/openapi2"
	"github.com/ghodss/yaml"
)

func transposeFileI(rootDir string, f os.FileInfo) {
	transposeFileN(rootDir, f.Name())
}

func transposeFileN(rootDir string, name string) {
	fname := path.Join(rootDir, name)
	log.Println("transposing ", fname)

	var swagger2 openapi2.Swagger

	yamlFile, err := ioutil.ReadFile(fname)
	if err != nil {
		log.Printf("yamlFile.Get err   #%v ", err)
	}

	err = yaml.Unmarshal(yamlFile, &swagger2)
	if err != nil {
		log.Fatalf("Unmarshal: %v", err)
		panic(err)
	}

	actualV3, err := openapi2conv.ToV3Swagger(&swagger2)
	if err != nil {
		log.Fatalf("Convert: %v", err)
	}

	data, err := yaml.Marshal(actualV3)
	//data, err := yaml.Marshal(swagger2)
	if err != nil {
		log.Fatalf("Json: %v", err)
	}

	print(string(data))

	println("Done.")

}

func transpose(root, api string) {
	dir := path.Join(root, "api", api)

	files, err := ioutil.ReadDir(dir)
	if err != nil {
		log.Fatalf("Error parsing directory: %v", err)
	}

	for _, f := range files {
		if strings.HasSuffix(f.Name(), ".yaml") {
			transposeFileI(dir, f)
		}
	}
}

func main() {
	root := "../ext-src/matrix-doc/"
	transpose(root, "application-service")
	transpose(root, "client-server")
	transpose(root, "identity")
	transpose(root, "push-gateway")
	transpose(root, "server-server")
}
