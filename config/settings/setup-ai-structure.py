#!/usr/bin/env python3
"""
AI Documentation Structure Setup and Management Tool

This script provides a command-line interface for managing the AI documentation
structure, including initialization, migration, and validation of documentation.
"""

import os
import sys
import argparse
import logging
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.setup.ai_structure_config import AIStructureConfig
from src.setup.initialize_structure import create_initial_docs
from src.utils.doc_migrator import DocumentationMigrator

def setup_logging(level: str = "INFO") -> None:
    """Configure logging for the setup process."""
    logging.basicConfig(
        level=getattr(logging, level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('ai_structure_setup.log'),
            logging.StreamHandler()
        ]
    )

def initialize_structure(args: argparse.Namespace) -> None:
    """Initialize the AI documentation structure."""
    logger = logging.getLogger("initialize")
    try:
        config = AIStructureConfig(args.config)
        create_initial_docs()
        logger.info("AI documentation structure initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize structure: {e}")
        raise

def migrate_docs(args: argparse.Namespace) -> None:
    """Migrate existing documentation to the new structure."""
    logger = logging.getLogger("migrate")
    try:
        migrator = DocumentationMigrator(Path.cwd())
        migrator.migrate_all_docs()
        logger.info("Documentation migration completed successfully")
    except Exception as e:
        logger.error(f"Failed to migrate documentation: {e}")
        raise

def validate_structure(args: argparse.Namespace) -> None:
    """Validate the AI documentation structure."""
    logger = logging.getLogger("validate")
    config = AIStructureConfig()
    
    # Check required directories
    required_dirs = [
        config.ai_docs_dir,
        config.config_dir,
        config.logs_dir,
        config.src_dir,
        config.ai_docs_dir / "voice" / "tts",
        config.ai_docs_dir / "voice" / "stt",
        config.ai_docs_dir / "calls" / "scenarios",
        config.ai_docs_dir / "calls" / "responses",
        config.ai_docs_dir / "comparisons"
    ]
    
    missing_dirs = [d for d in required_dirs if not d.exists()]
    if missing_dirs:
        logger.error("Missing required directories:")
        for d in missing_dirs:
            logger.error(f"  - {d}")
        raise ValueError("Invalid structure: missing directories")
    
    # Check required files
    required_files = [
        config.ai_docs_dir / "README.md",
        config.config_dir / "settings" / "default_config.yaml"
    ]
    
    missing_files = [f for f in required_files if not f.exists()]
    if missing_files:
        logger.error("Missing required files:")
        for f in missing_files:
            logger.error(f"  - {f}")
        raise ValueError("Invalid structure: missing files")
    
    logger.info("Structure validation completed successfully")

def main():
    """Main entry point for the AI structure management tool."""
    parser = argparse.ArgumentParser(
        description="AI Documentation Structure Management Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        default='INFO',
        help='Set logging level'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Initialize command
    init_parser = subparsers.add_parser('init', help='Initialize AI documentation structure')
    init_parser.add_argument('--config', type=Path, help='Path to custom config file')
    
    # Migrate command
    migrate_parser = subparsers.add_parser('migrate', help='Migrate existing documentation')
    
    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate structure')
    
    args = parser.parse_args()
    setup_logging(args.log_level)
    
    if args.command == 'init':
        initialize_structure(args)
    elif args.command == 'migrate':
        migrate_docs(args)
    elif args.command == 'validate':
        validate_structure(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
