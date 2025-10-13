-- Create a function to execute arbitrary SQL queries
-- This allows us to query system tables and run any SQL through RPC

CREATE OR REPLACE FUNCTION execute_sql_query(query_text text)
RETURNS json
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
    result json;
BEGIN
    -- Execute the query and return results as JSON
    EXECUTE format('SELECT json_agg(row_to_json(t)) FROM (%s) t', query_text) INTO result;
    
    -- If no results, return empty array
    IF result IS NULL THEN
        result := '[]'::json;
    END IF;
    
    RETURN result;
EXCEPTION
    WHEN OTHERS THEN
        -- Return error information
        RETURN json_build_object(
            'error', true,
            'message', SQLERRM,
            'detail', SQLSTATE
        );
END;
$$;

-- Grant execute permission to authenticated and service role
GRANT EXECUTE ON FUNCTION execute_sql_query(text) TO authenticated, service_role;

-- Create a simpler function for getting table list
CREATE OR REPLACE FUNCTION get_table_list()
RETURNS json
LANGUAGE sql
SECURITY DEFINER
AS $$
    SELECT json_agg(
        json_build_object(
            'schema', schemaname,
            'table', tablename,
            'owner', tableowner
        )
    )
    FROM pg_tables
    WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
    ORDER BY schemaname, tablename;
$$;

GRANT EXECUTE ON FUNCTION get_table_list() TO authenticated, service_role;