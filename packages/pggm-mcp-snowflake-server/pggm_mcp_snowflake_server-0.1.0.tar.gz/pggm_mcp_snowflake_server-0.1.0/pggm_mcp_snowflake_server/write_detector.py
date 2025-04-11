class SQLWriteDetector:
    """Utility class to detect write operations in SQL queries."""

    def __init__(self):
        self.write_keywords = [
            "INSERT", "UPDATE", "DELETE", "DROP", "CREATE", "ALTER", "TRUNCATE",
            "GRANT", "REVOKE", "MERGE", "UPSERT", "REPLACE"
        ]
    
    def analyze_query(self, query: str) -> dict:
        """
        Analyze an SQL query to determine if it contains write operations.
        
        Args:
            query: SQL query string to analyze
            
        Returns:
            Dictionary with analysis results
        """
        result = {
            "contains_write": False,
            "write_operations": [],
            "query_type": "READ"
        }
        
        # Convert to uppercase for case-insensitive comparison
        upper_query = query.upper()
        
        # Check for write keywords
        for keyword in self.write_keywords:
            if keyword in upper_query.split():
                result["contains_write"] = True
                result["write_operations"].append(keyword)
                result["query_type"] = "WRITE"
                
        return result
