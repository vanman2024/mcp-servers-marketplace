# Figma MCP Server Reorganization Plan

## Current State Analysis
- **Total files**: 10,510+ (DISASTER)
- **Python files**: 4,589 (Many duplicates and temp files)
- **SQL files**: 94 (Migration and batch files scattered)
- **JSON files**: 47 (Various config and data files)

## Proposed Directory Structure

```
figma-mcp/
├── src/                          # Core server code
│   ├── __init__.py
│   ├── figma_server_db.py        # MAIN SERVER FILE
│   ├── figma_server.py           # HTTP server
│   ├── figma_client.py           # Figma API client
│   ├── database_integration.py   # Database layer
│   ├── component_mapper.py       # Component mapping
│   ├── design_normalizer.py      # Design normalization
│   ├── file_generator.py         # File generation
│   ├── supabase_storage.py       # Storage layer
│   ├── theme_system.py           # Theme management
│   ├── navigation_system.py      # Navigation
│   └── page_generator.py         # Page generation
│
├── migrations/                   # Database migrations
│   ├── 001_initial_schema.sql
│   ├── 002_sections_architecture.sql
│   ├── 003_marketing_sections.sql
│   └── scripts/
│       ├── apply_migration.py
│       ├── migrate_to_sections.py
│       └── cleanup_duplicates.py
│
├── data/                         # Data files and imports
│   ├── taxonomies/
│   │   ├── tailwind_ui_taxonomy.json
│   │   ├── application_ui_taxonomy.json
│   │   └── shadcn_component_templates.json
│   ├── extracted/
│   │   ├── marketing_sections/
│   │   ├── application_ui/
│   │   └── templates/
│   ├── batches/
│   │   ├── pending/
│   │   ├── processing/
│   │   └── completed/
│   └── imports/
│       ├── tailwind_templates/
│       ├── marketing_data/
│       └── component_mappings/
│
├── scripts/                      # Utility scripts
│   ├── import/
│   │   ├── bulk_import_application_ui.py
│   │   ├── paste_component_helper.py
│   │   ├── extract_tailwind_templates.py
│   │   └── import_marketing_sections.py
│   ├── maintenance/
│   │   ├── cleanup_duplicates.py
│   │   ├── remove_temp_files.py
│   │   └── validate_database.py
│   ├── scrapers/
│   │   ├── scrape_tailwind_ui.py
│   │   ├── scrape_with_login.py
│   │   └── tailwind_cookies.py
│   └── generators/
│       ├── generate_bulk_sql.py
│       ├── create_component_batches.py
│       └── auto_insert_batches.py
│
├── tests/                        # Test files
│   ├── test_server.py
│   ├── test_database.py
│   ├── test_components.py
│   └── integration/
│       ├── test_figma_integration.py
│       └── test_supabase_integration.py
│
├── docs/                         # Documentation
│   ├── README.md
│   ├── API_REFERENCE.md
│   ├── DEPLOYMENT.md
│   ├── TROUBLESHOOTING.md
│   └── ARCHITECTURE.md
│
├── config/                       # Configuration files
│   ├── config.json
│   ├── requirements.txt
│   └── .env.example
│
└── temp/                         # Temporary files (gitignored)
    ├── logs/
    ├── cache/
    └── processing/
```

## Reorganization Strategy

### Phase 1: Core Server Files
1. **Keep in src/**: All essential server files
2. **Move to src/**: Any Python files that are part of the main server logic

### Phase 2: Database & Migrations
1. **Create migrations/**: Move all SQL files here
2. **Group by purpose**: Schema, data imports, cleanup
3. **Keep only latest**: Archive old migration attempts

### Phase 3: Data Organization
1. **Create data/**: All JSON configs, taxonomies, extracted data
2. **Batch management**: Organize all batch files by status
3. **Import data**: Separate raw data from processed data

### Phase 4: Scripts & Tools
1. **Import scripts**: All bulk import and data processing
2. **Maintenance**: Cleanup and validation scripts
3. **Scrapers**: All web scraping related files
4. **Generators**: SQL and batch generation scripts

### Phase 5: Clean Root Directory
1. **Move everything**: Root should only have essential files
2. **Keep only**: README.md, requirements.txt, main server files
3. **Archive old**: Move outdated files to archive/

## Files to Archive (Not Delete)
- All batch_*.json files → data/batches/completed/
- All chunk_*.sql files → data/batches/completed/
- All insert_batch_*.sql → data/batches/completed/
- All marketing_batch_*.sql → data/batches/completed/
- All phase1_*.sql → migrations/archive/
- All exec_batch_*.sql → migrations/archive/
- All test_*.py → tests/
- All *.log files → temp/logs/

## Priority Actions
1. **Create new directory structure**
2. **Move core server files first**
3. **Organize data files**
4. **Archive completed batches**
5. **Clean up duplicates**
6. **Update imports and paths**

## Benefits
- **Maintainable**: Clear separation of concerns
- **Scalable**: Easy to add new features
- **Debuggable**: Know where everything is
- **Professional**: Standard project structure
- **Efficient**: No more searching through thousands of files

## Execution Plan
1. Create new directory structure
2. Move files systematically (no deletion)
3. Update import paths
4. Test server functionality
5. Archive old structure
6. Update documentation

This will reduce the root directory from 100+ files to ~10 essential files.