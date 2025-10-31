-- Verification Queries for Phase 1 Migration

-- Check total block count
SELECT COUNT(*) as total_blocks FROM application_blocks WHERE app_type = 'e-commerce';

-- Check blocks by type
SELECT block_type, COUNT(*) as count 
FROM application_blocks 
WHERE app_type = 'e-commerce' 
GROUP BY block_type 
ORDER BY count DESC;

-- List all e-commerce blocks
SELECT name, block_type, created_at 
FROM application_blocks 
WHERE app_type = 'e-commerce' 
ORDER BY name;

-- Check for any missing dependencies
SELECT name, dependencies 
FROM application_blocks 
WHERE app_type = 'e-commerce' 
AND dependencies::text LIKE '%components%';
