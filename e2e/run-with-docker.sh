#!/bin/bash
# building docker image
docker build . --tag flashtest:1

# running a container 
docker run --rm flashtest:1 npx cypress run