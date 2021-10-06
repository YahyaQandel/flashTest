#!/bin/bash
# building docker image
docker-compose build e2e

# running a container 
if [ "$?" -eq "0" ]
then
    docker-compose run --rm e2e npx cypress run
else
  echo "failed to build system testing image , exiting ..."
fi