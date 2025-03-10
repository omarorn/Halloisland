#!/bin/bash
# RunPod deployment script with SSH key authentication
set -euo pipefail

SSH_KEY="${HOME}/.ssh/id_ed25519"
RUNPOD_USER="jm93erb48roquc-644118ca"
RUNPOD_HOST="ssh.runpod.io"
DEPLOY_DIR="/workspace/icelandic-voice"

# Validate SSH key permissions
chmod 600 "${SSH_KEY}"

# Deploy with atomic directory swap pattern
rsync -avzhe "ssh -i ${SSH_KEY} -o StrictHostKeyChecking=no" \
  --exclude=.git \
  --exclude=podcast_output \
  --exclude=.env \
  ./ ${RUNPOD_USER}@${RUNPOD_HOST}:${DEPLOY_DIR}.new/

# Atomic deployment switch
ssh -i "${SSH_KEY}" -T ${RUNPOD_USER}@${RUNPOD_HOST} <<EOF
  rm -rf ${DEPLOY_DIR}.old
  mv ${DEPLOY_DIR} ${DEPLOY_DIR}.old || true
  mv ${DEPLOY_DIR}.new ${DEPLOY_DIR}
  cd ${DEPLOY_DIR}
  docker-compose down
  docker-compose up -d --build
EOF

echo "Deployment completed successfully to RunPod"