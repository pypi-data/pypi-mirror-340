#!/bin/bash
set -e

# Load the .env file
set -o allexport
source .env

# Check if PYPI_OPENPIPE_TOKEN is set
if [[ -z "${PYPI_OPENPIPE_TOKEN}" ]]; then
    echo "Error: PYPI_OPENPIPE_TOKEN is not set."
    exit 1
fi

# Build the package
uv run hatch build


# If the token is set, proceed with publishing
uv publish --username=__token__ --password=$PYPI_OPENPIPE_TOKEN
