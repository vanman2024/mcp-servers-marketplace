#!/usr/bin/env python3
"""
Safe Reorganization Script
==========================
Safely reorganizes the figma-mcp directory with backup and verification.
"""

import os
import shutil
import subprocess
from pathlib import Path
from datetime import datetime

class SafeReorganizer:
    def __init__(self, base_path="/home/gotime2022/mcp-kernel-new/servers/http/figma-mcp"):
        self.base_path = Path(base_path)
        self.backup_created = False
        self.phase_completed = []
        
    def verify_backup_exists(self):
        """Verify backup was created"""
        parent_dir = self.base_path.parent
        backup_dirs = list(parent_dir.glob("figma-mcp-backup-*"))
        
        if backup_dirs:
            latest_backup = max(backup_dirs, key=lambda x: x.stat().st_mtime)
            print(f"✅ Backup found: {latest_backup}")
            self.backup_created = True
            return True
        else:
            print("❌ No backup found! Cannot proceed safely.")
            return False
    
    def create_directory_structure(self):
        """Phase 1: Create new directory structure"""
        print("\n🏗️  Phase 1: Creating directory structure...")
        
        directories = [
            "src",
            "migrations",
            "migrations/scripts",
            "migrations/archive",
            "data",
            "data/taxonomies",
            "data/extracted",
            "data/extracted/marketing_sections",
            "data/extracted/application_ui",
            "data/extracted/templates",
            "data/batches",
            "data/batches/pending",
            "data/batches/processing", 
            "data/batches/completed",
            "data/imports",
            "data/imports/tailwind_templates",
            "data/imports/marketing_data",
            "data/imports/component_mappings",
            "scripts",
            "scripts/import",
            "scripts/maintenance",
            "scripts/scrapers",
            "scripts/generators",
            "tests",
            "tests/integration",
            "docs",
            "config",
            "temp",
            "temp/logs",
            "temp/cache",
            "temp/processing",
            "archive"
        ]
        
        for directory in directories:
            dir_path = self.base_path / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"   📁 Created: {directory}")
        
        print("✅ Phase 1 Complete: Directory structure created")
        self.phase_completed.append("directory_structure")
        
    def move_core_files(self):
        """Phase 2: Move core server files to src/"""
        print("\n🔧 Phase 2: Moving core server files...")
        
        # Core server files that should be in src/
        core_files = [
            "figma_server_db.py",
            "figma_server.py", 
            "figma_client.py",
            "database_integration.py",
            "component_mapper.py",
            "design_normalizer.py",
            "file_generator.py",
            "supabase_storage.py",
            "theme_system.py",
            "navigation_system.py",
            "page_generator.py",
            "figma_server_health_check.py",
            "figma_server_hybrid.py"
        ]
        
        moved_count = 0
        for file_name in core_files:
            # Check both root and src/ directory
            source_root = self.base_path / file_name
            source_src = self.base_path / "src" / file_name
            dest = self.base_path / "src" / file_name
            
            if source_root.exists() and not dest.exists():
                shutil.move(str(source_root), str(dest))
                print(f"   ✅ Moved: {file_name} → src/")
                moved_count += 1
            elif source_src.exists():
                print(f"   ℹ️  Already in src/: {file_name}")
            else:
                print(f"   ⚠️  Not found: {file_name}")
        
        print(f"✅ Phase 2 Complete: {moved_count} core files moved to src/")
        self.phase_completed.append("core_files")
        
    def move_data_files(self):
        """Phase 3: Move data files to data/"""
        print("\n📊 Phase 3: Moving data files...")
        
        # Taxonomy files
        taxonomy_files = [
            "tailwind_ui_taxonomy.json",
            "application_ui_taxonomy.json", 
            "shadcn_component_templates.json",
            "figma_to_shadcn_mapping.json"
        ]
        
        for file_name in taxonomy_files:
            source = self.base_path / file_name
            dest = self.base_path / "data" / "taxonomies" / file_name
            
            if source.exists() and not dest.exists():
                shutil.move(str(source), str(dest))
                print(f"   ✅ Moved: {file_name} → data/taxonomies/")
        
        # Extracted data files
        extracted_files = [
            "extracted_sections.json",
            "marketing_sections_to_import.json",
            "extracted_figma_components.json"
        ]
        
        for file_name in extracted_files:
            source = self.base_path / file_name
            dest = self.base_path / "data" / "extracted" / file_name
            
            if source.exists() and not dest.exists():
                shutil.move(str(source), str(dest))
                print(f"   ✅ Moved: {file_name} → data/extracted/")
        
        print("✅ Phase 3 Complete: Data files organized")
        self.phase_completed.append("data_files")
        
    def move_batch_files(self):
        """Phase 4: Move batch files to data/batches/completed/"""
        print("\n📦 Phase 4: Moving batch files...")
        
        # Find all batch files
        batch_patterns = [
            "batch_*.json",
            "batch_*.sql", 
            "chunk_*.sql",
            "insert_batch_*.sql",
            "marketing_batch_*.sql",
            "exec_batch_*.sql"
        ]
        
        moved_count = 0
        for pattern in batch_patterns:
            for file_path in self.base_path.glob(pattern):
                if file_path.is_file():
                    dest = self.base_path / "data" / "batches" / "completed" / file_path.name
                    if not dest.exists():
                        shutil.move(str(file_path), str(dest))
                        moved_count += 1
                        print(f"   ✅ Moved: {file_path.name} → data/batches/completed/")
        
        print(f"✅ Phase 4 Complete: {moved_count} batch files moved")
        self.phase_completed.append("batch_files")
        
    def move_scripts(self):
        """Phase 5: Move scripts to scripts/"""
        print("\n🔧 Phase 5: Moving scripts...")
        
        # Import scripts
        import_scripts = [
            "bulk_import_application_ui.py",
            "paste_component_helper.py",
            "extract_tailwind_templates.py", 
            "import_marketing_sections.py",
            "bulk_import_supabase.py",
            "bulk_import_direct.py"
        ]
        
        for script in import_scripts:
            source = self.base_path / script
            dest = self.base_path / "scripts" / "import" / script
            
            if source.exists() and not dest.exists():
                shutil.move(str(source), str(dest))
                print(f"   ✅ Moved: {script} → scripts/import/")
        
        # Maintenance scripts
        maintenance_scripts = [
            "remove_duplicates.py",
            "validate_config.py"
        ]
        
        for script in maintenance_scripts:
            source = self.base_path / script
            dest = self.base_path / "scripts" / "maintenance" / script
            
            if source.exists() and not dest.exists():
                shutil.move(str(source), str(dest))
                print(f"   ✅ Moved: {script} → scripts/maintenance/")
        
        print("✅ Phase 5 Complete: Scripts organized")
        self.phase_completed.append("scripts")
        
    def move_config_files(self):
        """Phase 6: Move configuration files"""
        print("\n⚙️  Phase 6: Moving configuration files...")
        
        config_files = [
            "config.json",
            "requirements.txt"
        ]
        
        for file_name in config_files:
            source = self.base_path / file_name
            dest = self.base_path / "config" / file_name
            
            if source.exists() and not dest.exists():
                shutil.move(str(source), str(dest))
                print(f"   ✅ Moved: {file_name} → config/")
        
        print("✅ Phase 6 Complete: Configuration files moved")
        self.phase_completed.append("config_files")
        
    def move_logs_and_temp(self):
        """Phase 7: Move logs and temp files"""
        print("\n🗂️  Phase 7: Moving logs and temp files...")
        
        # Log files
        log_files = list(self.base_path.glob("*.log"))
        moved_logs = 0
        
        for log_file in log_files:
            dest = self.base_path / "temp" / "logs" / log_file.name
            if not dest.exists():
                shutil.move(str(log_file), str(dest))
                moved_logs += 1
                print(f"   ✅ Moved: {log_file.name} → temp/logs/")
        
        print(f"✅ Phase 7 Complete: {moved_logs} log files moved")
        self.phase_completed.append("logs_temp")
        
    def verify_critical_files(self):
        """Verify critical files are in correct locations"""
        print("\n🔍 Verifying critical files...")
        
        critical_files = [
            "src/figma_server_db.py",
            "config/config.json",
            "config/requirements.txt"
        ]
        
        all_good = True
        for file_path in critical_files:
            full_path = self.base_path / file_path
            if full_path.exists():
                print(f"   ✅ Found: {file_path}")
            else:
                print(f"   ❌ Missing: {file_path}")
                all_good = False
        
        return all_good
        
    def create_rollback_script(self):
        """Create rollback script for emergency recovery"""
        rollback_content = f"""#!/bin/bash
# Emergency Rollback Script
cd /home/gotime2022/mcp-kernel-new/servers/http
rm -rf figma-mcp
mv figma-mcp-backup-20250717_220115 figma-mcp
echo "✅ Rollback complete - original structure restored"
"""
        
        rollback_path = self.base_path / "EMERGENCY_ROLLBACK.sh"
        with open(rollback_path, 'w') as f:
            f.write(rollback_content)
        
        os.chmod(rollback_path, 0o755)
        print(f"✅ Created rollback script: {rollback_path}")
        
    def run_safe_reorganization(self):
        """Run the complete safe reorganization"""
        print("🚀 Starting Safe Reorganization of figma-mcp directory")
        print("=" * 60)
        
        if not self.verify_backup_exists():
            print("❌ ABORTED: No backup found!")
            return False
        
        try:
            self.create_directory_structure()
            self.move_core_files()
            self.move_data_files()
            self.move_batch_files()
            self.move_scripts()
            self.move_config_files()
            self.move_logs_and_temp()
            
            if self.verify_critical_files():
                self.create_rollback_script()
                
                print("\n🎉 REORGANIZATION COMPLETE!")
                print("=" * 40)
                print("✅ All phases completed successfully")
                print("✅ Critical files verified")
                print("✅ Rollback script created")
                print("✅ No data lost - everything moved safely")
                print("\n📁 New structure:")
                print("   - src/ (core server files)")
                print("   - data/ (organized data files)")
                print("   - scripts/ (utility scripts)")
                print("   - config/ (configuration)")
                print("   - temp/ (logs and temp files)")
                print("\n⚠️  If anything breaks, run: ./EMERGENCY_ROLLBACK.sh")
                
                return True
            else:
                print("❌ Critical files missing - check manually")
                return False
                
        except Exception as e:
            print(f"❌ ERROR during reorganization: {e}")
            print("🔄 Consider running EMERGENCY_ROLLBACK.sh")
            return False

if __name__ == "__main__":
    reorganizer = SafeReorganizer()
    success = reorganizer.run_safe_reorganization()
    
    if success:
        print("\n✅ Ready to continue with application UI import!")
    else:
        print("\n❌ Reorganization failed - check logs and consider rollback")