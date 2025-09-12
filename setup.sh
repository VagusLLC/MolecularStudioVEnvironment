#!/bin/bash

# Install pixi using curl (fallback to wget if curl fails)
echo "Installing pixi..."
if command -v curl >/dev/null 2>&1; then
    curl -fsSL https://pixi.sh/install.sh | sh
elif command -v wget >/dev/null 2>&1; then
    wget -qO- https://pixi.sh/install.sh | sh
else
    echo "Error: Neither curl nor wget is available. Please install one of them."
    exit 1
fi

# Clone the repository and navigate to it
echo "Cloning MolecularStudioVEnvironment repository..."
git clone https://github.com/VagusLLC/MolecularStudioVEnvironment.git && cd MolecularStudioVEnvironment

# Run pixi setup commands
echo "Running pixi setup..."
pixi run setup

echo "Running pixi fireworks_setup..."
pixi run fireworks_setup

echo "Setup completed successfully!"
