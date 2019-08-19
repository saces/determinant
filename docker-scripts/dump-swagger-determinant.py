#!/usr/bin/env python3

# dump-swagger-determinant reads all of the swagger API docs used in spec generation and
# outputs YAML files for use as input for code generators.

import argparse
import errno
import json
import logging
import os.path
import re
import sys
import yaml

parser = argparse.ArgumentParser(
    "dump-swagger-determinant.py - assemble the Swagger specs for code generation"
)
parser.add_argument(
    "--client_release", "-c", metavar="LABEL",
    default="unstable",
    help="""The client-server release version to gneerate for. Default:
    %(default)s""",
)
parser.add_argument(
    "-t", "--target", metavar="TARGET_DIR", required=True,
    help="Directory to write the output to."
)
parser.add_argument(
    "-d", "--api-dir", metavar="API_DIR", required=True,
    help="Directory with the matrix api spec."
)

args = parser.parse_args()

output_dir = os.path.abspath(args.target)
try:
    os.makedirs(output_dir)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

release_label = args.client_release

major_version = release_label
match = re.match("^(r\d+)(\.\d+)*$", major_version)
if match:
    major_version = match.group(1)

logging.basicConfig()

output_c2s = {
    "basePath": "/",
    "consumes": ["application/json"],
    "produces": ["application/json"],
    "host": "matrix.org",
    "schemes": ["https"],
    "info": {
        "title": "Matrix Client-Server API",
        "version": release_label,
    },
    "securityDefinitions": {},
    "paths": {},
    "swagger": "2.0",
}

output_s2s = {
    "basePath": "/",
    "consumes": ["application/json"],
    "produces": ["application/json"],
    "host": "matrix.org",
    "schemes": ["https"],
    "info": {
        "title": "Matrix Federation API",
        "version": release_label,
    },
    "securityDefinitions": {},
    "paths": {},
    "swagger": "2.0",
}

output_as = {
    "basePath": "/",
    "consumes": ["application/json"],
    "produces": ["application/json"],
    "host": "matrix.org",
    "schemes": ["https"],
    "info": {
        "title": "Matrix Aplication Service API",
        "version": release_label,
    },
    "securityDefinitions": {},
    "paths": {},
    "swagger": "2.0",
}

output_push = {
    "swagger": "2.0",
    "info": {
        "title": "Matrix Push Notification API",
        "version": "1.0.0",
    },
    "host": "localhost:8008",
    "schemes": ["http", "https"],
    "consumes": ["application/json"],
    "produces": ["application/json"],
    "basePath": "/",
    "paths": {},
}

output_identity = {
    "swagger": "2.0",
    "info": {
        "title": "Matrix Identity Service API",
        "version": "1.0.0",
    },
    "host": "localhost:8090",
    "schemes": ["https"],
    "consumes": ["application/json"],
    "produces": ["application/json"],
    "basePath": "/",
    "paths": {},
}

def resolve_references(path, schema):
    if isinstance(schema, dict):
        # do $ref first
        if '$ref' in schema:
            value = schema['$ref']
            print("RefResolve: %s" % value)
            path = os.path.join(os.path.dirname(path), value)
            with open(path, encoding="utf-8") as f:
                ref = yaml.full_load(f)
            result = resolve_references(path, ref)
            del schema['$ref']
        else:
            result = {}

        for key, value in schema.items():
            result[key] = resolve_references(path, value)
        return result
    elif isinstance(schema, list):
        return [resolve_references(path, value) for value in schema]
    else:
        return schema

def dump_api(apiname, output, client_major_version=None):
    in_dir = os.path.join(args.api_dir, 'api', apiname)
    output_file = os.path.join(output_dir, apiname + '.swagger.yaml')
    
    for filename in os.listdir(in_dir):
        if not filename.endswith(".yaml"):
            continue
        filepath = os.path.join(in_dir, filename)

        print("Reading swagger API: %s" % filepath)
        with open(filepath, "r") as f:
            api = yaml.full_load(f.read())
            api = resolve_references(filepath, api)

            basePath = api['basePath']
            for path, methods in api["paths"].items():
                if client_major_version:
                    path = (basePath + path).replace('%CLIENT_MAJOR_VERSION%', client_major_version)
                else:
                    path = basePath + path
                #print("Path: %s" % path)
                
                for method, spec in methods.items():
                    #if "tags" in spec.keys():
                    if path not in output["paths"]:
                        output["paths"][path] = {}
                    output["paths"][path][method] = spec

    print("Generating %s" % output_file)

    with open(output_file, "w") as f:
        text = yaml.safe_dump(output, default_flow_style=False, canonical=False, default_style='"')
        #text = text.replace("%CLIENT_RELEASE_LABEL%", release_label)
        #text = text.replace("%CLIENT_MAJOR_VERSION%", major_version)
        f.write(text)


dump_api('push-gateway', output_push)
dump_api('server-server', output_s2s)
dump_api('application-service', output_as)
dump_api('client-server', output_c2s, major_version)
dump_api('identity', output_identity)

print("Generating spec files done. Bye.")
