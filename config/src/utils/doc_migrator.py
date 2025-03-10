#!/usr/bin/env python3
from pathlib import Path
import re
import logging
import shutil
from datetime import datetime
from typing import List, Dict, Optional

class DocumentationMigrator:
    """Utility class to migrate existing documentation to the new structure."""
    
    def __init__(self, base_dir: Path):
        """
        Initialize the documentation migrator.
        
        Args:
            base_dir: Base directory containing the AI documentation
        """
        self.base_dir = base_dir
        self.backup_dir = base_dir / "backup"
        self.setup_logging()
        
    def setup_logging(self) -> None:
        """Configure logging for the migration process."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.base_dir / "logs/migration.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger("doc_migrator")
    
    def backup_existing_docs(self) -> None:
        """Create a backup of existing documentation."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.backup_dir / f"backup_{timestamp}"
        
        self.logger.info(f"Creating backup at: {backup_path}")
        shutil.copytree(self.base_dir, backup_path, dirs_exist_ok=True)
    
    def categorize_document(self, content: str) -> str:
        """
        Determine the appropriate category for a document based on its content.
        
        Args:
            content: The document content to analyze
            
        Returns:
            String indicating the document category
        """
        content_lower = content.lower()
        
        if any(term in content_lower for term in ['tts', 'text-to-speech', 'voice synthesis']):
            return 'voice/tts'
        elif any(term in content_lower for term in ['stt', 'speech-to-text', 'transcription']):
            return 'voice/stt'
        elif any(term in content_lower for term in ['call', 'phone', 'response']):
            return 'calls/scenarios'
        elif any(term in content_lower for term in ['comparison', 'versus', 'vs']):
            return 'comparisons'
        else:
            return ''
    
    def migrate_document(self, source_path: Path) -> None:
        """
        Migrate a single document to the new structure.
        
        Args:
            source_path: Path to the document to migrate
        """
        try:
            with open(source_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            category = self.categorize_document(content)
            if not category:
                self.logger.warning(f"Could not categorize document: {source_path}")
                return
            
            # Determine new path
            new_dir = self.base_dir / "ai-docs" / category
            new_path = new_dir / source_path.name
            
            # Ensure directory exists
            new_dir.mkdir(parents=True, exist_ok=True)
            
            # Move file to new location
            shutil.move(str(source_path), str(new_path))
            self.logger.info(f"Migrated {source_path.name} to {category}")
            
        except Exception as e:
            self.logger.error(f"Failed to migrate {source_path}: {e}")
    
    def migrate_all_docs(self) -> None:
        """Migrate all markdown documentation to the new structure."""
        try:
            # Create backup first
            self.backup_existing_docs()
            
            # Find all markdown files
            md_files = list(self.base_dir.glob("**/*.md"))
            self.logger.info(f"Found {len(md_files)} markdown files to migrate")
            
            # Migrate each file
            for file_path in md_files:
                if not any(p.name.startswith('.') for p in file_path.parents):
                    self.migrate_document(file_path)
            
            self.logger.info("Documentation migration completed successfully")
            
        except Exception as e:
            self.logger.error(f"Migration failed: {e}")
            raise

def main():
    """Main entry point for the documentation migration tool."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Migrate documentation to new structure")
    parser.add_argument('--dir', type=Path, default=Path.cwd(),
                      help="Base directory containing the documentation")
    args = parser.parse_args()
    
    migrator = DocumentationMigrator(args.dir)
    migrator.migrate_all_docs()

if __name__ == "__main__":
    main()