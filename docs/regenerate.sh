#!/usr/bin/env bash
ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
sphinx-apidoc -f -o $ROOT/source $ROOT/../scripts/pickrunner
