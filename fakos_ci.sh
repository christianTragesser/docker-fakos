#!/bin/bash

set -e

SCRIPT=`basename "$0"`
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [ ! $# == 1 ]; then
    printf "\n $SCRIPT script needs a parameter: unit, test, etc. \n ex: '$SCRIPT test' \n\n"
    exit 1
fi

OPTION=$1
NETWORK="ci_net"
CYAN='\033[1;36m'
PURPLE='\033[1;35m'
NC='\033[0m'

function ci {
  case $OPTION in
    unit) unit
    ;;
    test) unit
          build
    ;;
    *) printf "\n *** Selection $OPTION not found, exiting. ***\n\n"
          exit 1
  esac
}

function unit {
  docker run --rm -i -v $SCRIPT_DIR:/tmp -w /tmp/docker/test christiantragesser/dind-ci pytest
}

function build {
  cd $SCRIPT_DIR/docker && docker build -t christiantragesser/fakos .
}

ci