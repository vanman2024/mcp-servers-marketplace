# SRC Directory Analysis

## Current Files (27 total)

### 🔥 CORE SERVER FILES (Keep - Essential)
1. **figma_server_db.py** - Main MCP server (CRITICAL)
2. **figma_server.py** - HTTP server 
3. **figma_client.py** - Figma API client
4. **database_integration.py** - Database layer
5. **supabase_storage.py** - Storage layer
6. **__init__.py** - Package initialization

### 🎨 FEATURE MODULES (Keep - Current Features)
7. **component_mapper.py** - Maps components
8. **design_normalizer.py** - Normalizes designs
9. **file_generator.py** - Generates files
10. **page_generator.py** - Generates pages
11. **navigation_system.py** - Navigation handling
12. **theme_system.py** - Theme management
13. **theme_system_enhanced.py** - Enhanced themes
14. **new_sections_functions.py** - New sections functionality

### 🔧 UTILITY/HEALTH FILES (Keep - Operational)
15. **figma_server_health_check.py** - Health monitoring
16. **figma_server_hybrid.py** - Hybrid functionality

### 📊 DATA FILES (Move to data/)
17. **phase1_ecommerce_blocks_complete.json** → `data/extracted/`
18. **migration_phase1_complete_ecommerce.sql** → `migrations/archive/`

### 🗂️ LOG FILES (Move to temp/logs/)
19. **figma_db_server.log** → `temp/logs/`
20. **figma_server.log** → `temp/logs/`

### 🔄 VERSION FILES (Consolidate or Archive)
21. **figma_server_db_backup_20250717_194130.py** → `archive/backups/`
22. **figma_server_db_sections_complete_update.py** → `archive/versions/`
23. **figma_server_db_sections_update.py** → `archive/versions/`
24. **figma_server_db_update.py** → `archive/versions/`

### 📈 EXPANSION FILES (Move to scripts/)
25. **block_expansion_phase1.py** → `scripts/generators/`
26. **block_expansion_phase1_part2.py** → `scripts/generators/`
27. **block_expansion_phase1_part3.py** → `scripts/generators/`
28. **block_expansion_phase1_part4.py** → `scripts/generators/`
29. **generate_all_ecommerce_blocks.py** → `scripts/generators/`

## 🎯 PROPOSED CONSOLIDATION

### After Cleanup - Core src/ (14 files):
```
src/
├── __init__.py
├── figma_server_db.py          # MAIN SERVER
├── figma_server.py             # HTTP SERVER
├── figma_client.py             # FIGMA API
├── database_integration.py     # DATABASE
├── supabase_storage.py         # STORAGE
├── component_mapper.py         # COMPONENTS
├── design_normalizer.py        # DESIGN
├── file_generator.py           # FILES
├── page_generator.py           # PAGES
├── navigation_system.py        # NAVIGATION
├── theme_system.py             # THEMES
├── figma_server_health_check.py # HEALTH
└── new_sections_functions.py   # SECTIONS
```

### 🤔 CONSOLIDATION OPPORTUNITIES

#### Theme System
- **Current**: `theme_system.py` + `theme_system_enhanced.py`
- **Proposed**: Merge into single `theme_system.py`
- **Why**: Avoid confusion about which to use

#### Server Files
- **Current**: `figma_server_hybrid.py` might be redundant
- **Check**: Is this needed or can functionality be in main server?

## 📋 CLEANUP ACTIONS

1. **Move Data Files** (2 files) → `data/extracted/`
2. **Move Log Files** (2 files) → `temp/logs/`
3. **Archive Version Files** (4 files) → `archive/versions/`
4. **Move Expansion Scripts** (5 files) → `scripts/generators/`
5. **Consider Consolidating** theme files
6. **Review** hybrid server file necessity

## 🎯 RESULT
- **From**: 27 files (confusing)
- **To**: ~14 files (clean, focused)
- **Benefit**: Clear, maintainable, professional structure

## ⚠️ SAFETY
- No deletion - everything moved to appropriate locations
- All functionality preserved
- Easy rollback available