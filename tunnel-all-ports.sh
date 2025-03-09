#!/bin/bash

# This script creates port forwarding for multiple Pinokio ports
# and configures Pinokio to listen on all interfaces

# Define the ports you want to forward
PORTS=(42000 3000 3001 3333 4000 5000 5678 7861 8000 8080 8888 9000)

# First, stop any existing tunnel services
sudo systemctl stop port-tunnel 2>/dev/null || true
sudo systemctl disable port-tunnel 2>/dev/null || true

# Create a tunnel service for each port
for PORT in "${PORTS[@]}"; do
  SERVICE_NAME="port-tunnel-${PORT}"
  
  # Create service file
  cat > /tmp/${SERVICE_NAME}.conf << EOF
[Unit]
Description=Port Forwarding for Port ${PORT}
After=network.target

[Service]
ExecStart=/usr/bin/socat TCP-LISTEN:${PORT},fork,reuseaddr TCP:0.0.0.0:${PORT}
Restart=always
RestartSec=5
User=azureuser

[Install]
WantedBy=multi-user.target
EOF

  # Install and start the service
  sudo mv /tmp/${SERVICE_NAME}.conf /etc/systemd/system/${SERVICE_NAME}.service
  sudo systemctl enable ${SERVICE_NAME}
  sudo systemctl start ${SERVICE_NAME}
  
  # Open firewall for this port
  sudo iptables -A INPUT -p tcp --dport ${PORT} -j ACCEPT
  
  echo "Port ${PORT} forwarding configured and started"
done

# Save iptables rules
sudo iptables-save | sudo tee /etc/iptables/rules.v4 > /dev/null

# Ensure Pinokio is configured to listen on all interfaces
cd /home/azureuser/pinokio
NODE_PATH=$(which node)
$NODE_PATH -e '
const fs = require("fs");
const path = require("path");
const packageJsonPath = path.join(process.cwd(), "package.json");

try {
  // Create a custom package.json config that allows external access
  const pkg = require(packageJsonPath);
  if (!pkg.pinokio) pkg.pinokio = {};
  pkg.pinokio.host = "0.0.0.0";
  pkg.pinokio.port = 42000;
  fs.writeFileSync(packageJsonPath, JSON.stringify(pkg, null, 2));
  console.log("Pinokio configured for external access on all interfaces");
} catch (err) {
  console.error("Error configuring Pinokio:", err);
}
'

echo "All ports have been opened and forwarded."
echo "Pinokio main interface is available at http://aiserver.swedencentral.cloudapp.azure.com:42000/"
echo "Additional services will be available on their respective ports."