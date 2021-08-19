#!/bin/bash

sudo apt install -y python3.8-venv

PYTHON_INTERPRETER=python3
VIRTUAL_ENV_DIR=venv

set -e

${PYTHON_INTERPRETER} --version

echo '========== Install Python env =========='
${PYTHON_INTERPRETER} -m venv ${VIRTUAL_ENV_DIR}
source ${VIRTUAL_ENV_DIR}/bin/activate
${PYTHON_INTERPRETER} -m pip install --upgrade pip

bash ./setup.sh
