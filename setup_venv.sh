#!/bin/bash

# Get the absolute, fully dereferenced path of this script file
SCRIPT_PATH=$(realpath "${BASH_SOURCE[0]:-$0}")
# Get the absolute path of the directory containing this script
SCRIPT_DIR=$(dirname "$SCRIPT_PATH")
echo "Script File: $SCRIPT_PATH"
echo "Script Directory: $SCRIPT_DIR"

python3 -m venv "${SCRIPT_DIR}"/.venv
printf "Setting up python virtual environment in %s/.venv now ...\n" "${SCRIPT_DIR}"
# shellcheck disable=SC1091
source "${SCRIPT_DIR}"/.venv/bin/activate
yes | pip install fastapi uvicorn pydantic
printf "\nThe script will come out of venv on exit. To reenter it, run the following command:\nsource %s/.venv/bin/activate\n" "${SCRIPT_DIR}"
printf "\nPlease run command **deactivate** to come out of it, when done.\n\nTo use this venv in VS code, please run Ctrl+Shift+P > Python: Select Interpreter > .venv/bin/python\n"
