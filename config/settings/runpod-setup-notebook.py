{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# RunPod AI Development Environment Setup\n",
    "\n",
    "This notebook will guide you through setting up your RunPod environment for AI development, ensuring you're ready to use those L40 GPUs effectively. We'll cover:\n",
    "\n",
    "1. Verifying your hardware and GPU setup\n",
    "2. Installing and setting up key AI libraries\n",
    "3. Configuring environment variables and paths\n",
    "4. Testing your setup with a simple model\n",
    "5. Setting up persistent storage\n",
    "\n",
    "Let's get started!"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 1. System Verification\n",
    "\n",
    "First, let's check our system configuration to ensure everything is properly detected."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Check system configuration\n",
    "!nvidia-smi"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Check CPU and memory\n",
    "!cat /proc/cpuinfo | grep \"model name\" | uniq\n",
    "!grep MemTotal /proc/meminfo"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Check disk space\n",
    "!df -h /workspace"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 2. Install Required Libraries\n",
    "\n",
    "Let's install the essential libraries for AI development. You can customize this list based on your specific needs."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Update pip\n",
    "!pip install --upgrade pip"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Install deep learning frameworks\n",
    "!pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Install Hugging Face libraries\n",
    "!pip install transformers datasets accelerate xformers bitsandbytes"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Install helper libraries\n",
    "!pip install pandas matplotlib seaborn scikit-learn scipy jupyter jupyterlab tqdm"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Install other useful libraries \n",
    "!pip install wandb peft gradio sentencepiece sacremoses safetensors tiktoken einops"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 3. Verify CUDA and PyTorch Setup\n",
    "\n",
    "Let's confirm that PyTorch can detect and use our GPUs."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import torch\n",
    "import sys\n",
    "\n",
    "print(f\"Python version: {sys.version}\")\n",
    "print(f\"PyTorch version: {torch.__version__}\")\n",
    "print(f\"CUDA available: {torch.cuda.is_available()}\")\n",
    "print(f\"CUDA version: {torch.version.cuda}\")\n",
    "print(f\"Number of GPUs: {torch.cuda.device_count()}\")\n",
    "\n",
    "for i in range(torch.cuda.device_count()):\n",
    "    print(f\"GPU {i}: {torch.cuda.get_device_name(i)}\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 4. Configure Environment Variables\n",
    "\n",
    "Setting up environment variables that may be needed for specific frameworks or tools."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import os\n",
    "\n",
    "# Set cache directories to point to the persistent storage\n",
    "os.environ[\"TRANSFORMERS_CACHE\"] = \"/workspace/.cache/huggingface/transformers\"\n",
    "os.environ[\"HF_DATASETS_CACHE\"] = \"/workspace/.cache/huggingface/datasets\"\n",
    "os.environ[\"HF_HOME\"] = \"/workspace/.cache/huggingface\"\n",
    "\n",
    "# Create the cache directories if they don't exist\n",
    "!mkdir -p $TRANSFORMERS_CACHE\n",
    "!mkdir -p $HF_DATASETS_CACHE\n",
    "\n",
    "# Set PyTorch to use deterministic algorithms when possible\n",
    "os.environ[\"CUBLAS_WORKSPACE_CONFIG\"] = \":4096:8\"\n",
    "\n",
    "print(\"Environment variables configured successfully!\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 5. Setup Persistent Storage\n",
    "\n",
    "Ensure we're using the persistent volume for our work and cache."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Create project directories\n",
    "!mkdir -p /workspace/projects\n",
    "!mkdir -p /workspace/datasets\n",
    "!mkdir -p /workspace/models\n",
    "!mkdir -p /workspace/.cache\n",
    "\n",
    "print(\"Directory structure created!\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 6. Test GPU with a Simple Model\n",
    "\n",
    "Let's run a quick test to ensure our GPUs are working properly with a simple model from Hugging Face."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "from transformers import AutoModel, AutoTokenizer\n",
    "import torch\n",
    "import time\n",
    "\n",
    "# Load a small model for testing\n",
    "model_name = \"distilbert-base-uncased\"\n",
    "print(f\"Loading {model_name}...\")\n",
    "\n",
    "tokenizer = AutoTokenizer.from_pretrained(model_name)\n",
    "model = AutoModel.from_pretrained(model_name)\n",
    "\n",
    "# Move model to GPU\n",
    "device = torch.device(\"cuda\" if torch.cuda.is_available() else \"cpu\")\n",
    "model = model.to(device)\n",
    "print(f\"Model loaded and moved to {device}\")\n",
    "\n",
    "# Prepare input\n",
    "text = \"Testing my GPU setup for AI development on RunPod!\"\n",
    "encoded_input = tokenizer(text, return_tensors=\"pt\")\n",
    "encoded_input = {k: v.to(device) for k, v in encoded_input.items()}\n",
    "\n",
    "# Run inference and measure time\n",
    "start_time = time.time()\n",
    "with torch.no_grad():\n",
    "    output = model(**encoded_input)\n",
    "end_time = time.time()\n",
    "\n",
    "print(f\"Inference time: {(end_time - start_time) * 1000:.2f} ms\")\n",
    "print(\"GPU test successful!\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 7. Multi-GPU Setup\n",
    "\n",
    "Since your RunPod has 2 L40 GPUs, let's test multi-GPU capabilities."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "if torch.cuda.device_count() > 1:\n",
    "    print(f\"Setting up model for {torch.cuda.device_count()} GPUs\")\n",
    "    # Load a larger model to showcase multi-GPU capabilities\n",
    "    from transformers import AutoModelForCausalLM\n",
    "    \n",
    "    model_name = \"facebook/opt-1.3b\"  # A medium-sized model good for testing\n",
    "    print(f\"Loading {model_name} for multi-GPU test...\")\n",
    "    \n",
    "    model = AutoModelForCausalLM.from_pretrained(model_name)\n",
    "    # Use DataParallel for multi-GPU\n",
    "    model = torch.nn.DataParallel(model)\n",
    "    model = model.to(device)\n",
    "    \n",
    "    print(\"Multi-GPU setup complete!\")\n",
    "    \n",
    "    # Verify each GPU is being utilized\n",
    "    print(\"\\nGPU utilization after model loading:\")\n",
    "    !nvidia-smi --query-gpu=index,name,utilization.gpu,memory.used --format=csv\n",
    "else:\n",
    "    print(\"Multi-GPU setup skipped as only one GPU is available.\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 8. Setup Git for Version Control\n",
    "\n",
    "Let's configure Git to manage your projects."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Configure Git (replace with your details)\n",
    "!git config --global user.name \"Your Name\"\n",
    "!git config --global user.email \"your.email@example.com\"\n",
    "!git config --global init.defaultBranch main\n",
    "\n",
    "print(\"Git configured successfully!\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 9. Create a Sample Project Structure\n",
    "\n",
    "Let's create a template project structure to get you started quickly."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "!mkdir -p /workspace/projects/sample_project\n",
    "!mkdir -p /workspace/projects/sample_project/data\n",
    "!mkdir -p /workspace/projects/sample_project/models\n",
    "!mkdir -p /workspace/projects/sample_project/scripts\n",
    "!mkdir -p /workspace/projects/sample_project/notebooks\n",
    "\n",
    "# Create a readme file\n",
    "readme_content = \"\"\"# Sample AI Project\n",
    "\n",
    "This is a template project structure for AI development on RunPod.\n",
    "\n",
    "## Directory Structure\n",
    "- `data/`: For datasets and processed data\n",
    "- `models/`: For saving trained models\n",
    "- `scripts/`: Python scripts for training, evaluation, etc.\n",
    "- `notebooks/`: Jupyter notebooks for exploration and visualization\n",
    "\"\"\"\n",
    "\n",
    "with open(\"/workspace/projects/sample_project/README.md\", \"w\") as f:\n",
    "    f.write(readme_content)\n",
    "\n",
    "print(\"Sample project structure created at /workspace/projects/sample_project/\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 10. Setup Automated Backup\n",
    "\n",
    "Since RunPod spot instances can be terminated, let's create a simple backup script."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "%%writefile /workspace/backup.sh\n",
    "#!/bin/bash\n",
    "\n",
    "# Simple backup script for RunPod workspace\n",
    "BACKUP_DIR=\"/workspace/backups\"\n",
    "TIMESTAMP=$(date +\"%Y%m%d_%H%M%S\")\n",
    "BACKUP_FILE=\"${BACKUP_DIR}/workspace_backup_${TIMESTAMP}.tar.gz\"\n",
    "\n",
    "# Create backup directory if it doesn't exist\n",
    "mkdir -p \"${BACKUP_DIR}\"\n",
    "\n",
    "# Create tar archive of projects folder\n",
    "tar -czf \"${BACKUP_FILE}\" -C /workspace projects\n",
    "\n",
    "echo \"Backup created: ${BACKUP_FILE}\"\n",
    "\n",
    "# Remove backups older than 7 days\n",
    "find \"${BACKUP_DIR}\" -name \"workspace_backup_*.tar.gz\" -mtime +7 -delete\n",
    "echo \"Old backups cleaned up\""
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Make the backup script executable\n",
    "!chmod +x /workspace/backup.sh\n",
    "\n",
    "# Create a directory for backups\n",
    "!mkdir -p /workspace/backups\n",
    "\n",
    "print(\"Backup script created and configured!\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 11. Final System Check\n",
    "\n",
    "Let's do a final system check to make sure everything is working as expected."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "print(\"======= FINAL SYSTEM CHECK =======\\n\")\n",
    "\n",
    "# Check CUDA and GPU\n",
    "print(\"GPU Information:\")\n",
    "!nvidia-smi --query-gpu=name,memory.total,memory.free,driver_version --format=csv,noheader\n",
    "\n",
    "# Check Python and installed packages\n",
    "print(\"\\nPython Version:\")\n",
    "!python --version\n",
    "\n",
    "print(\"\\nPyTorch and CUDA:\")\n",
    "print(f\"PyTorch: {torch.__version__}\")\n",
    "print(f\"CUDA available: {torch.cuda.is_available()}\")\n",
    "print(f\"CUDA version: {torch.version.cuda}\")\n",
    "\n",
    "print(\"\\nInstalled AI Packages:\")\n",
    "!pip list | grep -E \"torch|transformers|datasets|sklearn|pandas|matplotlib|huggingface|gradio|accelerate|xformers\"\n",
    "\n",
    "print(\"\\nStorage:\")\n",
    "!df -h /workspace\n",
    "\n",
    "print(\"\\n======= SYSTEM READY FOR AI DEVELOPMENT =======\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 12. Getting Started Guidance\n",
    "\n",
    "Here are some next steps and suggestions for your AI development:\n",
    "\n",
    "1. **Load your datasets:**\n",
    "   - Place your datasets in `/workspace/datasets/`\n",
    "   - Use Hugging Face's `datasets` library to access popular datasets directly\n",
    "\n",
    "2. **Start developing in projects:**\n",
    "   - Use the project template in `/workspace/projects/sample_project/`\n",
    "   - Create new project directories as needed\n",
    "\n",
    "3. **Monitor GPU usage:**\n",
    "   - Run `nvidia-smi` to check GPU utilization\n",
    "   - Use `watch -n 1 nvidia-smi` for continuous monitoring\n",
    "\n",
    "4. **Backup your work:**\n",
    "   - Run `/workspace/backup.sh` periodically\n",
    "   - Consider pushing to a git repository regularly\n",
    "\n",
    "5. **Manage large models:**\n",
    "   - Use `accelerate` and `bitsandbytes` for memory-efficient training\n",
    "   - Leverage techniques like 8-bit quantization or LoRA for fine-tuning\n",
    "\n",
    "6. **For multi-GPU training:**\n",
    "   - Use PyTorch's `DataParallel` for simple parallelism\n",
    "   - For more complex needs, use `DistributedDataParallel` or Hugging Face's `Accelerate`\n",
    "\n",
    "7. **Visualize results:**\n",
    "   - Create notebooks in project directories for visualizations\n",
    "   - Consider using tools like Weights & Biases (`wandb`) for experiment tracking\n",
    "\n",
    "Enjoy your AI development on RunPod!"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.10.12"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
