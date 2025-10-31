#!/usr/bin/env python3
"""
Clean Root Directory - Phase 2
==============================
Move all remaining files from root to proper locations
"""

import os
import shutil
from pathlib import Path

class RootDirectoryCleaner:
    def __init__(self, base_path="/home/gotime2022/mcp-kernel-new/servers/http/figma-mcp"):
        self.base_path = Path(base_path)
        
    def clean_root_directory(self):
        """Move all remaining files from root to proper locations"""
        print("🧹 Cleaning Root Directory - Phase 2")
        print("=" * 50)
        
        # Files that should stay in root
        keep_in_root = {
            'README.md',
            'EMERGENCY_ROLLBACK.sh',
            'start.sh',
            '.gitignore',
            'BACKUP_SAFETY_PROTOCOL.md',
            'REORGANIZATION_PLAN.md'
        }
        
        # Directories that should stay in root
        keep_dirs = {
            'src', 'data', 'scripts', 'config', 'temp', 'tests', 'docs', 'migrations', 'archive'
        }
        
        moved_count = 0
        
        # Get all items in root
        root_items = list(self.base_path.iterdir())
        
        for item in root_items:
            if item.name in keep_in_root or item.name in keep_dirs:
                continue
                
            if item.is_file():
                moved_count += self._move_file(item)
            elif item.is_dir():
                moved_count += self._move_directory(item)
        
        print(f"\n✅ Root cleanup complete! Moved {moved_count} items")
        self._show_clean_root()
        
    def _move_file(self, file_path):
        """Move a single file to appropriate location"""
        file_name = file_path.name
        
        # Migration files
        if file_name.endswith('.sql') and any(x in file_name for x in ['migration', 'phase1', 'remaining']):
            dest = self.base_path / 'migrations' / 'archive' / file_name
            shutil.move(str(file_path), str(dest))
            print(f"   📦 {file_name} → migrations/archive/")
            return 1
            
        # Other SQL files (setup, bulk operations)
        elif file_name.endswith('.sql'):
            dest = self.base_path / 'scripts' / 'generators' / file_name
            shutil.move(str(file_path), str(dest))
            print(f"   🔧 {file_name} → scripts/generators/")
            return 1
            
        # Python scripts
        elif file_name.endswith('.py'):
            if any(x in file_name for x in ['import', 'bulk', 'extract', 'sync']):
                dest = self.base_path / 'scripts' / 'import' / file_name
                shutil.move(str(file_path), str(dest))
                print(f"   📥 {file_name} → scripts/import/")
                return 1
            elif any(x in file_name for x in ['test', 'validate']):
                dest = self.base_path / 'tests' / file_name
                shutil.move(str(file_path), str(dest))
                print(f"   🧪 {file_name} → tests/")
                return 1
            elif any(x in file_name for x in ['scrape', 'cookies']):
                dest = self.base_path / 'scripts' / 'scrapers' / file_name
                shutil.move(str(file_path), str(dest))
                print(f"   🕷️  {file_name} → scripts/scrapers/")
                return 1
            elif any(x in file_name for x in ['execute', 'apply', 'create', 'generate']):
                dest = self.base_path / 'scripts' / 'generators' / file_name
                shutil.move(str(file_path), str(dest))
                print(f"   ⚙️  {file_name} → scripts/generators/")
                return 1
            else:
                dest = self.base_path / 'scripts' / 'maintenance' / file_name
                shutil.move(str(file_path), str(dest))
                print(f"   🔧 {file_name} → scripts/maintenance/")
                return 1
                
        # JSON files
        elif file_name.endswith('.json'):
            dest = self.base_path / 'data' / 'extracted' / file_name
            shutil.move(str(file_path), str(dest))
            print(f"   📊 {file_name} → data/extracted/")
            return 1
            
        # Documentation files
        elif file_name.endswith('.md'):
            dest = self.base_path / 'docs' / file_name
            shutil.move(str(file_path), str(dest))
            print(f"   📖 {file_name} → docs/")
            return 1
            
        # Text files and other configs
        elif file_name.endswith(('.txt', '.sh')):
            if file_name == 'start.sh':
                return 0  # Keep in root
            dest = self.base_path / 'config' / file_name
            shutil.move(str(file_path), str(dest))
            print(f"   ⚙️  {file_name} → config/")
            return 1
            
        # HTML/log files
        elif file_name.endswith(('.html', '.log')):
            dest = self.base_path / 'temp' / 'cache' / file_name
            shutil.move(str(file_path), str(dest))
            print(f"   🗂️  {file_name} → temp/cache/")
            return 1
            
        # Everything else goes to archive
        else:
            dest = self.base_path / 'archive' / file_name
            shutil.move(str(file_path), str(dest))
            print(f"   📦 {file_name} → archive/")
            return 1
            
    def _move_directory(self, dir_path):
        """Move a directory to appropriate location"""
        dir_name = dir_path.name
        
        # Test directories
        if 'test' in dir_name.lower():
            dest = self.base_path / 'tests' / dir_name
            shutil.move(str(dir_path), str(dest))
            print(f"   🧪 {dir_name}/ → tests/")
            return 1
            
        # Environment/virtual env directories
        elif dir_name in ['venv', 'test_env', '.venv']:
            dest = self.base_path / 'temp' / dir_name
            shutil.move(str(dir_path), str(dest))
            print(f"   🔧 {dir_name}/ → temp/")
            return 1
            
        # Everything else goes to archive
        else:
            dest = self.base_path / 'archive' / dir_name
            shutil.move(str(dir_path), str(dest))
            print(f"   📦 {dir_name}/ → archive/")
            return 1
            
    def _show_clean_root(self):
        """Show what's left in root directory"""
        print("\n📁 Clean Root Directory Contents:")
        print("-" * 30)
        
        root_items = sorted([item.name for item in self.base_path.iterdir()])
        for item in root_items:
            if item.startswith('.'):
                continue
            print(f"   {item}")
            
        print(f"\n✅ Root directory now has {len(root_items)} items (should be ~10)")

if __name__ == "__main__":
    cleaner = RootDirectoryCleaner()
    cleaner.clean_root_directory()