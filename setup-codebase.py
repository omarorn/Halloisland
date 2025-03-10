import shutil
import os

def create_structure():
    # Define the base directory for the project
    base_dir = "/halloisland"

    # Define the folder structure
    folder_structure = {
        "halloisland": [
            "config",
            "data",
            "fine_tune",
            "agent",
            "deployment",
            "docs"
        ],
        "halloisland/config": ["config.yaml"],
        "halloisland/data": [],
        "halloisland/fine_tune": ["fine_tune_llm.py", "fine_tune_tts.py", "datasets.py"],
        "halloisland/agent": ["stt.py", "tts.py", "llm.py", "main.py"],
        "halloisland/deployment": ["server.py", "azure_bot_service.py", "docker-compose.yml", "Dockerfile"],
        "halloisland/docs": ["README.md", "setup_guide.md", "fine_tuning.md", "deployment_instructions.md"]
    }

    # Create the directory structure
    for folder, files in folder_structure.items():
        os.makedirs(os.path.join(base_dir, folder), exist_ok=True)
        for file in files:
            open(os.path.join(base_dir, folder, file), 'w').close()  # Create empty files

   