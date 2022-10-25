#!/bin/bash

script_path="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd ${script_path}

if [ ! -d "$script_path/venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source ${script_path}/venv/bin/activate
pip3 install -r $script_path/requirements.txt
