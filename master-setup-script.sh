#!/bin/bash
#################################################################
#                                                               #
#                Railway Setup Script                          #
#                                                               #
#   This script configures the environment for the Icelandic   #
#   voice application on Railway.                              #
#                                                               #
#################################################################

# Set error handling
set -e
trap 'echo "Error on line $LINENO. Exit code: $?" >&2' ERR

# Define colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

#################################################################
#                     Environment Setup                         #
#################################################################

log_info "Starting environment setup..."

# Install additional Python packages
log_info "Installing Python packages and AI tools..."
pip install --ignore-installed blinker
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install transformers datasets huggingface_hub
pip install gradio
pip install pandas numpy matplotlib scikit-learn
pip install openai langchain

# Install requirements from the project
if [ -f "requirements.txt" ]; then
    log_info "Installing Python requirements..."
    pip install --ignore-installed -r requirements.txt
    log_success "Project requirements installed"
fi

if [ -f "requirements_icelandic.txt" ]; then
    log_info "Installing Icelandic-specific requirements..."
    pip install --ignore-installed -r requirements_icelandic.txt
    log_success "Icelandic requirements installed"
fi

log_success "Environment setup complete!"
