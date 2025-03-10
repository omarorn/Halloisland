#!/usr/bin/env python3
from pathlib import Path
import argparse
import logging
from .ai_structure_config import AIStructureConfig  # Fixed relative import

def create_initial_docs() -> None:
    """Create initial documentation files in the new structure."""
    config = AIStructureConfig()
    
    # Create main README in ai-docs
    readme_content = """# Icelandic Voice Assistant Documentation

## Overview
This documentation covers the implementation of an Icelandic voice assistant system, including Text-to-Speech (TTS), Speech-to-Text (STT), and call handling capabilities.

## Directory Structure

```
ai-docs/
├── voice/
│   ├── tts/         # Text-to-Speech documentation
│   └── stt/         # Speech-to-Text documentation
├── calls/
│   ├── scenarios/   # Call handling scenarios
│   └── responses/   # AI response templates
└── comparisons/     # Technology comparisons
```

## Quick Start
1. Review the voice technology comparisons in `comparisons/`
2. Choose appropriate TTS/STT solutions from `voice/`
3. Implement call scenarios from `calls/scenarios/`
4. Test with response templates from `calls/responses/`

## Components
- Voice Technology (TTS/STT)
- Call Handling
- Response Management
- System Integration

## Configuration
See `config/settings/` for system configuration options.

## Logging
System logs are stored in:
- `logs/voice-logs/` for voice processing
- `logs/call-logs/` for call handling
"""
    
    readme_path = config.ai_docs_dir / "README.md"
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)

def main():
    parser = argparse.ArgumentParser(description='Initialize AI documentation structure')
    parser.add_argument('--config', type=Path, help='Path to custom config file')
    parser.add_argument('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                      default='INFO', help='Set logging level')
    args = parser.parse_args()
    
    # Initialize configuration
    try:
        config = AIStructureConfig(args.config)
        logging.basicConfig(level=getattr(logging, args.log_level))
        logger = logging.getLogger(__name__)
        
        # Create initial documentation
        create_initial_docs()
        
        logger.info("AI documentation structure initialized successfully")
        logger.info(f"Documentation directory: {config.ai_docs_dir}")
        logger.info(f"Configuration directory: {config.config_dir}")
        logger.info(f"Logs directory: {config.logs_dir}")
        
    except Exception as e:
        logging.error(f"Failed to initialize AI structure: {e}")
        raise

if __name__ == "__main__":
    main()