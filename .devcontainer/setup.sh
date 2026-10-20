#!/bin/bash
set -e

echo ">>> Setting up Python 3.11 Course Development Sandbox..."
python3 -m pip install --upgrade pip
python3 -m pip install pytest python-pptx

echo ">>> Environment setup complete. Python version:"
python3 --version
