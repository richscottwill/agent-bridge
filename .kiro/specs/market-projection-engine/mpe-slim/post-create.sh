#!/bin/bash
set -e

echo "🚀 Setting up MPE Bayesian Development Environment..."

# Update pip
pip install --upgrade pip

# Install requirements using internal Amazon PyPI mirror
if [ -f requirements.txt ]; then
    echo "📦 Installing Python packages from internal mirror..."
    pip install --no-cache-dir -r requirements.txt \
        --index-url https://your-internal-pypi.amazon.com/simple/ \
        --trusted-host your-internal-pypi.amazon.com
else
    echo "⚠️ requirements.txt not found. Skipping package installation."
fi

# Install additional useful tools
pip install --no-cache-dir \
    uv \
    ruff \
    black \
    mypy \
    pre-commit

# Create Jupyter kernel
python -m ipykernel install --user --name=mpe-bayesian --display-name "MPE Bayesian (Python 3.11)"

echo "✅ Environment setup complete!"
echo ""
echo "To start JupyterLab, run:"
echo "  jupyter lab --ip=0.0.0.0 --port=8888 --no-browser"
echo ""
echo "Or use the 'Jupyter: Create New Notebook' command in VS Code."