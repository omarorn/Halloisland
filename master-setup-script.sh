#!/bin/bash
#################################################################
#                                                               #
#                RunPod Master Setup Script                     #
#                                                               #
#   This script configures a full AI development environment    #
#   with n8n, Leon AI, and various development tools.           #
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

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

#################################################################
#                     Environment Setup                         #
#################################################################

log_info "Starting environment setup..."

# Create necessary directories
mkdir -p /workspace/ssl
mkdir -p /workspace/logs
mkdir -p /root/.ssh

# Update package lists
log_info "Updating package lists..."
apt update

# Install system dependencies and main tools
log_info "Installing system dependencies and tools..."
apt install -y git vim curl wget htop nodejs npm tmux screen unzip zip \
               build-essential cmake pkg-config python3-dev \
               net-tools iotop iftop ncdu ffmpeg \
               libopenblas-dev liblapack-dev openssh-client \
               python3-venv docker.io docker-compose \
               certbot openssl apache2-utils \
               nvidia-cuda-toolkit nvidia-cuda-dev cuda-command-line-tools

# Update pip
log_info "Updating pip..."
pip install --upgrade pip

#################################################################
#                 Python Packages Installation                  #
#################################################################

log_info "Installing Python packages and AI tools..."
pip install --ignore-installed blinker
pip install torch torchvision torchaudio
pip install transformers datasets huggingface_hub
pip install jupyter jupyterlab gradio
pip install pandas numpy matplotlib scikit-learn
pip install openai anthropic langchain

#################################################################
#                       SSH Key Setup                           #
#################################################################

log_info "Setting up SSH keys..."
cat > /root/.ssh/authorized_keys << 'END_PUBKEY'
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDFbqRwnJmjMVWVMXgo+LFJz0I44g/rz56r0sovFjxONnfbdNjpL90vJkBrTu2jxFGWFVZqnFX4pZt5vOw8DQC5Qu5LIFujeBbabvBU6vzVkQW630RlNbaHIeT2MNhJBCxycseXBpPQU4eXYnW8/kbFDcROKOjroBI+yWQROMVvjUqOVWzYeh+1e6HbCX/Ky3pILOHOEzPciegeQouyUv5qp7yPDavNy9M1iGozJd9jWo/Avi5DkB0bvvGZUmmD6XQw6YgGgoV+ssl1dY9syfR8C5UocSH9gheL9jrWHPZ946LVLSP99tt/xLMOg9je6j0avLE6eFFm3kQ973x+GGByLwDeqyD6lgqkxIOmO039Z1pgiO3Q2S6PR9hadFgFMSA23QnXtnd7TFtol9rYYqgez6ZnI+iyPB67wGhK0Q/E/5YXlJUvpmYEQ8dkukrWMPIDpGzLBkq7b7Q0XXXJPvwtLUPvT69b/dt0mkn9dFcnEt7a0yaznx7aZQfmKnSMaQk== omaromar@runpod
END_PUBKEY

chmod 700 /root/.ssh
chmod 600 /root/.ssh/authorized_keys
log_success "SSH key configured"

#################################################################
#                        SSL Setup                              #
#################################################################

log_info "Setting up SSL certificates..."
cd /workspace/ssl

# Create a self-signed certificate (as a fallback until Let's Encrypt is set up)
if [ ! -f "/workspace/ssl/server.key" ]; then
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout server.key -out server.crt \
        -subj "/CN=localhost"
    log_success "Self-signed certificate created"
fi

#################################################################
#                   CLI Tools Installation                      #
#################################################################

# Install Claude CLI
if [ ! -f "/usr/local/bin/claude" ]; then
    log_info "Installing Claude CLI..."
    curl -sSL https://github.com/anthropics/claude-cli/releases/latest/download/claude-cli_Linux_x86_64.tar.gz | tar xz -C /tmp
    mv /tmp/claude /usr/local/bin/
    chmod +x /usr/local/bin/claude
    log_success "Claude CLI installed"
fi

# Install Claude-code
log_info "Installing Claude Code..."
npm install -g claude-code
log_success "Claude Code installed"

#################################################################
#                 Repository Management                         #
#################################################################

# Clone n8n Self-Hosted AI Starter Kit
if [ -d "/workspace/self-hosted-ai-starter-kit" ]; then
    log_info "Updating n8n Self-Hosted AI Starter Kit..."
    cd /workspace/self-hosted-ai-starter-kit
    git pull
else
    log_info "Cloning n8n Self-Hosted AI Starter Kit..."
    git clone https://github.com/n8n-io/self-hosted-ai-starter-kit.git /workspace/self-hosted-ai-starter-kit
    
    # Configure SSL for the starter kit
    cd /workspace/self-hosted-ai-starter-kit
    # Update docker-compose to use SSL certificates
    if [ -f "docker-compose.yml" ]; then
        sed -i 's/80:5678/443:5678/g' docker-compose.yml
        # Add volumes for certificates if not already present
        grep -q "/workspace/ssl" docker-compose.yml || \
        sed -i '/n8n:/,/^\s*[a-z]/ s/volumes:/volumes:\n      - \/workspace\/ssl:\/etc\/ssl\/n8n/g' docker-compose.yml
    fi
    log_success "n8n Self-Hosted AI Starter Kit configured"
fi

# Clone or update Leon AI
if [ -d "/workspace/leon" ]; then
    log_info "Updating Leon AI..."
    cd /workspace/leon
    git pull
else
    log_info "Cloning Leon AI..."
    git clone https://github.com/leon-ai/leon.git /workspace/leon
    
    # Configure Leon to use HTTPS and listen on all interfaces
    cd /workspace/leon
    cp .env.sample .env
    echo "LEON_HOST=0.0.0.0" >> .env
    echo "LEON_PORT=1342" >> .env
    npm install
    npm run build
    log_success "Leon AI configured"
fi

# Clone or update halloisland repository
if [ -d "/workspace/halloisland" ]; then
    log_info "Updating halloisland repository..."
    cd /workspace/halloisland
    git pull
else
    log_info "Cloning halloisland repository..."
    git clone https://github.com/omarorn/halloisland.git /workspace/halloisland
fi

# Install requirements from the halloisland repository
if [ -f "/workspace/halloisland/requirements.txt" ]; then
    log_info "Installing Python requirements from halloisland..."
    pip install --ignore-installed -r /workspace/halloisland/requirements.txt
    log_success "halloisland requirements installed"
fi

#################################################################
#                   Firewall Configuration                      #
#################################################################

# Configure firewall (if available) to allow ports
if command -v ufw &> /dev/null; then
    log_info "Configuring firewall..."
    ufw allow 22/tcp    # SSH
    ufw allow 80/tcp    # HTTP
    ufw allow 443/tcp   # HTTPS
    ufw allow 1342/tcp  # Leon
    ufw allow 5678/tcp  # n8n
    ufw allow 8080/tcp  # n8n starter kit
    ufw allow 8888/tcp  # Jupyter
    ufw reload
    log_success "Firewall configured"
fi

#################################################################
#                     Autostart Script                          #
#################################################################

log_info "Setting up autostart script..."
cat > /workspace/autostart.sh << 'EOF'
#!/bin/bash

# Log file
LOGFILE="/workspace/logs/autostart.log"
exec > >(tee -a $LOGFILE) 2>&1

echo "$(date) - Starting services..."

# Start Docker service
service docker start || true
echo "$(date) - Docker service started"

# Start Jupyter Lab with SSL
cd /workspace
jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root \
  --certfile=/workspace/ssl/server.crt --keyfile=/workspace/ssl/server.key &
echo "$(date) - Jupyter Lab started"

# Start n8n Self-Hosted AI Starter Kit
cd /workspace/self-hosted-ai-starter-kit
docker-compose up -d
echo "$(date) - n8n Self-Hosted AI Starter Kit started"

# Start Leon AI
cd /workspace/leon
npm start &
echo "$(date) - Leon AI started"

# Try to obtain Let's Encrypt certificate if domain is available
if [ ! -z "$DOMAIN" ] && [ -x "$(command -v certbot)" ]; then
    echo "$(date) - Attempting to obtain Let's Encrypt certificate for $DOMAIN"
    certbot certonly --standalone --non-interactive --agree-tos \
      --email your@email.com -d $DOMAIN \
      --cert-path /workspace/ssl/letsencrypt \
      --deploy-hook "cp /workspace/ssl/letsencrypt/live/$DOMAIN/* /workspace/ssl/"
    echo "$(date) - Let's Encrypt certificate obtained"
fi

echo "$(date) - All services started!"
EOF

chmod +x /workspace/autostart.sh

# Add autostart to .bashrc for non-systemd environments
grep -q "autostart.sh" /root/.bashrc || echo '
# Autostart workspace services if not already running
if [ ! "$(pgrep jupyter)" ]; then
    echo "Starting workspace services..."
    bash /workspace/autostart.sh
fi
' >> /root/.bashrc

log_success "Autostart script configured"

#################################################################
#                   Start Services Now                          #
#################################################################

log_info "Running the autostart script to start all services..."
bash /workspace/autostart.sh

log_success "Environment setup complete!"
log_info "Your development environment is now ready!"
log_info "Jupyter Lab: https://your-runpod-url:8888"
log_info "n8n: https://your-runpod-url:5678"
log_info "Leon AI: http://your-runpod-url:1342"
