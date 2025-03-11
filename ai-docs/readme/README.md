# AI Documentation Structure Manager

## Local Development Setup

### Using Virtual Environment (Recommended for Local Development)

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On Unix/MacOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the tool
python setup-ai-structure.py init
python setup-ai-structure.py migrate
```

### Using Docker (Alternative Local Setup)

```bash
# Build the image
docker build -t ai-docs-manager .

# Run the container
docker run -v $(pwd):/app ai-docs-manager python setup-ai-structure.py init
docker run -v $(pwd):/app ai-docs-manager python setup-ai-structure.py migrate
```

### On RunPod or Server

When running on RunPod or other server environments where the dependencies are pre-installed:

```bash
# Direct execution
python setup-ai-structure.py init
python setup-ai-structure.py migrate
```

## Commands

### Initialize Structure

Creates the basic directory structure and configuration:

```bash
python setup-ai-structure.py init [--config path/to/config.yaml]
```

### Migrate Documentation

Organizes existing documentation into the new structure:

```bash
python setup-ai-structure.py migrate
```

### Validate Structure

Checks if the structure is valid:

```bash
python setup-ai-structure.py validate
```

## Directory Structure

```
.
├── ai-docs/
│   ├── voice/
│   │   ├── tts/         # Text-to-Speech documentation
│   │   └── stt/         # Speech-to-Text documentation
│   ├── calls/
│   │   ├── scenarios/   # Call handling scenarios
│   │   └── responses/   # AI response templates
│   └── comparisons/     # Technology comparisons
├── src/
│   ├── setup/          # Setup and initialization code
│   └── utils/          # Utility functions
├── config/
│   ├── templates/      # XML and other templates
│   └── settings/       # Configuration files
└── logs/
    ├── voice-logs/     # Voice processing logs
    └── call-logs/      # Call handling logs
```

## Dependencies

See `requirements.txt` for the full list of dependencies.

## Development

### Adding New Features

1. Create a new branch from main
2. Implement your changes
3. Add tests if applicable
4. Update documentation
5. Submit a pull request

### Testing

To run tests:

```bash
# In virtual environment
python -m pytest

# With Docker
docker run ai-docs-manager python -m pytest