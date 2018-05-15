#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

docker run --rm -it -v $SCRIPT_DIR:/tmp -w /tmp/docker/test christiantragesser/dind-ci pytest