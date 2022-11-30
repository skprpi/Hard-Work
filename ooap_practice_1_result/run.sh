#!/bin/bash

script_path="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd ${script_path}

if [ ! -d "$script_path/venv" ]; then
    echo "Run setup.sh first"
    exit 77
fi

source ${script_path}/venv/bin/activate
export PYTHONPATH=${script_path}
python3 ./main/main.py
