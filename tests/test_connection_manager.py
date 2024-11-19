"""
Tests for the database connection manager.
"""
import unittest
import os
from database.connection_manager import DatabaseConnectionManager

class TestDatabaseConnectionManager(unittest.TestCase):
    def setUp(self):
        self.manager = DatabaseConnectionManager()
        
    def test_connection_basic(self):
        """Test basic connection functionality."""
        positions = ['A1', 'B1', 'C1']  # Test with a few databases
        for pos in positions:
            with self.manager.get_connection(pos) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                self.assertEqual(result[0], 1)
                
    def test_table_names(self):
        """Test getting table names."""
        tables = self.manager.get_table_names('A1')
        self.assertTrue(len(tables) > 0)  # Should have at least one table
        self.assertIn('tokens', tables)  # A1 should have tokens table
        
    def test_execute_query(self):
        """Test query execution."""
        result = self.manager.execute_query('A1', "SELECT COUNT(*) as count FROM tokens")
        self.assertIsNotNone(result)
        
    def test_connection_retry(self):
        """Test connection retry mechanism."""
        # Try to connect to all databases
        success = 0
        for row in 'ABCDEFG':
            for col in range(1, 6):
                position = f"{row}{col}"
                if self.manager.check_connection(position):
                    success += 1
        self.assertEqual(success, 35)  # Should connect to all 35 databases
        
    def test_pool_reuse(self):
        """Test connection pool reuse."""
        position = 'A1'
        # Make multiple requests to test pool reuse
        for _ in range(10):
            with self.manager.get_connection(position) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                
    def tearDown(self):
        self.manager.close_all_connections()

if __name__ == '__main__':
    unittest.main()
