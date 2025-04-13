#!/bin/bash

# Create directory structure
mkdir -p src/pyqueuex
mkdir -p tests
mkdir -p docs
mkdir -p examples

# Create empty Python files in src/pyqueuex
touch src/pyqueuex/__init__.py
touch src/pyqueuex/queuex.py
touch src/pyqueuex/worker.py
touch src/pyqueuex/job.py
touch src/pyqueuex/strategies.py
touch src/pyqueuex/exceptions.py
touch src/pyqueuex/utils.py
touch src/pyqueuex/types.py

# Create test files
touch tests/__init__.py
touch tests/test_queuex.py
touch tests/test_worker.py

# Create docs files
touch docs/index.rst
touch docs/conf.py
touch docs/requirements.txt

# Create example file
touch examples/quick_start.py

# Create top-level files
touch README.md
touch LICENSE
touch pyproject.toml
touch CHANGELOG.md

echo "✅ Project structure created successfully."
