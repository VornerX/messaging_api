#!/bin/bash

docker build -t messaging-api-img:1.0 .
docker build -t messaging-api-img:1.0-TESTS -f Dockerfile.test .
