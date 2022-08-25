#!/usr/bin/env bash

echo "Mypy is running now "
python -m mypy --config-file setup.cfg

echo "Flake8 is running now"
python -m flake8 --config setup.cfg

echo "Done"
