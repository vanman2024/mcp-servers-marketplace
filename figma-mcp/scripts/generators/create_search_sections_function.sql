-- Create the search_sections RPC function for full-text search
CREATE OR REPLACE FUNCTION search_sections(
    search_query TEXT DEFAULT NULL,
    category_filter TEXT DEFAULT NULL,
    project_filter UUID DEFAULT NULL,
    limit_results INTEGER DEFAULT 20
)
RETURNS TABLE (
    id UUID,
    name VARCHAR(255),
    description TEXT,
    category VARCHAR(100),
    source VARCHAR(50),
    block_type VARCHAR(100),
    app_type VARCHAR(50),
    project_id UUID,
    is_template BOOLEAN,
    preview_url TEXT,
    created_at TIMESTAMPTZ,
    rank REAL
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        s.id,
        s.name,
        s.description,
        s.category,
        s.source,
        s.block_type,
        s.app_type,
        s.project_id,
        s.is_template,
        s.preview_url,
        s.created_at,
        CASE 
            WHEN search_query IS NULL THEN 1.0
            ELSE ts_rank(s.search_vector, plainto_tsquery('english', search_query))
        END as rank
    FROM sections s
    WHERE 
        (search_query IS NULL OR s.search_vector @@ plainto_tsquery('english', search_query))
        AND (category_filter IS NULL OR s.category = category_filter)
        AND (project_filter IS NULL OR s.project_id = project_filter OR s.is_template = true)
        AND s.published = true
    ORDER BY rank DESC, s.created_at DESC
    LIMIT limit_results;
END;
$$ LANGUAGE plpgsql;