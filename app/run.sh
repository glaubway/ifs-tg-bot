#!/usr/bin/env bash

echo "Running mypy "
python -m mypy --strict $(find /app/ -type f -name '*.py')