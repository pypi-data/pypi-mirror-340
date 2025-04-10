# tests/test_integration_git.py - Updated test class

import os
import tempfile
import unittest
import subprocess
import shutil

from credscan.history.scanner import HistoryScanner

class TestHistoryScanningIntegration(unittest.TestCase):
    """Integration tests for git history scanning."""
    
    def setUp(self):
        """Set up the test environment."""
        # Create a temporary directory
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_dir = self.temp_dir.name
        self.original_dir = os.getcwd()
        
        # Create a git repository with history
        self.create_test_repository()
        
        # Configuration
        self.config = {
            'verbose': True,
            'repo_path': self.test_dir  # Explicitly set repo path
        }
    
    def tearDown(self):
        """Clean up the test environment."""
        os.chdir(self.original_dir)
        self.temp_dir.cleanup()
    
    def create_test_repository(self):
        """Create a test git repository with a history of credentials."""
        # Initialize repository
        os.chdir(self.test_dir)
        subprocess.run(["git", "init"], check=True)
        subprocess.run(["git", "config", "user.name", "Test User"], check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], check=True)
        
        # Create initial files
        os.makedirs("config", exist_ok=True)
        
        # Initial commit - no credentials
        with open("config/settings.py", "w") as f:
            f.write("# Initial settings\nDEBUG = True\n")
        
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "Initial commit"], check=True)
        
        # Second commit - add API key
        with open("config/settings.py", "w") as f:
            f.write("# Settings with API key\nDEBUG = True\nAPI_KEY = 'api_secret_12345'\n")
        
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "Add API key to settings"], check=True)
        
        # Third commit - add database password
        with open("config/database.py", "w") as f:
            f.write("# Database settings\nDB_HOST = 'localhost'\nDB_PASSWORD = 'super_secret_db_pass'\n")
        
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "Add database configuration"], check=True)
        
        # Fourth commit - remove API key but keep password
        with open("config/settings.py", "w") as f:
            f.write("# Settings without API key\nDEBUG = True\n")
        
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "Remove API key"], check=True)
        
        # Return to original directory
        os.chdir(self.original_dir)
    
    def test_history_scanning(self):
        """Test complete history scanning process."""
        # Save current directory
        original_dir = os.getcwd()
        
        try:
            # Change to the test repository directory
            os.chdir(self.test_dir)
            
            # Run the history scanner
            scanner = HistoryScanner(self.config)
            # Explicitly set the repo root
            scanner.repo_root = self.test_dir
            
            # Print debugging information
            print(f"Running in directory: {os.getcwd()}")
            print(f"Repository path: {scanner.repo_root}")
            print(f".git exists: {os.path.exists(os.path.join(scanner.repo_root, '.git'))}")
            
            findings = scanner.scan()
            
            # Print findings for debugging
            print(f"Found {len(findings)} findings in history:")
            for i, finding in enumerate(findings):
                print(f"Finding {i+1}: {finding.get('variable', 'N/A')} = {finding.get('value', 'N/A')}")
            
            # Verify we found both credentials
            self.assertGreaterEqual(len(findings), 2, "Should find at least 2 credentials in history")
            
            # Check for specific credentials
            api_key_found = False
            db_password_found = False
            
            for finding in findings:
                if "api_key" in finding.get("variable", "").lower() and "api_secret_12345" in finding.get("value", ""):
                    api_key_found = True
                elif "password" in finding.get("variable", "").lower() and "super_secret_db_pass" in finding.get("value", ""):
                    db_password_found = True
            
            self.assertTrue(api_key_found, "API key not found in history")
            self.assertTrue(db_password_found, "Database password not found in history")
        
        finally:
            # Change back to original directory
            os.chdir(original_dir)

if __name__ == "__main__":
    unittest.main()