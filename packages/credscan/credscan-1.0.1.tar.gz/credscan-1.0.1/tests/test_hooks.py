"""
Tests for the git hooks integration.
"""
import os
import tempfile
import unittest
from unittest.mock import patch, MagicMock, call
import subprocess

from credscan.hooks import PreCommitScanner, install_hook

class TestPreCommitHook(unittest.TestCase):
    """Test pre-commit hook functionality."""
    
    def setUp(self):
        """Set up the test environment."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_dir = self.temp_dir.name
        
        # Create sample files with credentials
        self.create_test_files()
        
        # Default config
        self.config = {
            'verbose': True,
            'hook_config': 'warning-only',
            'hook_use_baseline': False
        }
    
    def tearDown(self):
        """Clean up the test environment."""
        self.temp_dir.cleanup()
    
    def create_test_files(self):
        """Create test files with credentials for testing."""
        # Create a JSON file with credentials
        os.makedirs(os.path.join(self.test_dir, "src"), exist_ok=True)
        
        # Sample JSON file
        json_content = """
        {
            "apiKey": "api_key_1234567890abcdef",
            "password": "super_secret_password"
        }
        """
        json_path = os.path.join(self.test_dir, "src", "config.json")
        with open(json_path, "w") as f:
            f.write(json_content)
    
    @patch('subprocess.run')
    def test_get_repo_root(self, mock_run):
        """Test getting the git repository root directory."""
        # Setup mock
        process_mock = MagicMock()
        process_mock.stdout = "/path/to/repo\n"
        mock_run.return_value = process_mock
        
        # Create scanner with repo_root already set to avoid initialization call
        scanner = PreCommitScanner(self.config)
        # Override the repo_root that was set during initialization
        scanner.repo_root = None
        
        # Now test the method explicitly
        root = scanner._get_repo_root()
        
        # Verify
        self.assertEqual(root, "/path/to/repo")
        # Check the last call instead of asserting called once
        mock_run.assert_called_with(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=True
        )
    
    @patch('subprocess.run')
    def test_get_staged_files(self, mock_run):
        """Test getting the staged files."""
        # Setup mock
        process_mock = MagicMock()
        process_mock.stdout = "file1.py\nfile2.json\n"
        mock_run.return_value = process_mock
        
        # Create scanner with repo_root already set to avoid initialization call
        scanner = PreCommitScanner(self.config)
        # Set repo_root directly to avoid another subprocess call
        scanner.repo_root = "/path/to/repo"
        
        # Run the test
        files = scanner.get_staged_files()
        
        # Verify
        self.assertEqual(files, ["file1.py", "file2.json"])
        # Check only the last call
        self.assertEqual(
            mock_run.call_args_list[-1],
            call(
                ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
                capture_output=True,
                text=True,
                check=True
            )
        )
    
    @patch('credscan.hooks.pre_commit.PreCommitScanner.get_staged_files')
    @patch('credscan.hooks.pre_commit.PreCommitScanner._get_repo_root')
    @patch('os.path.exists')
    @patch('os.path.join')
    def test_scan_staged_files(self, mock_join, mock_exists, mock_get_root, mock_get_files):
        """Test scanning staged files for credentials."""
        # Setup mocks
        mock_get_root.return_value = self.test_dir
        mock_get_files.return_value = ["src/config.json"]
        
        # Mock the os.path.join to return the exact file path we need
        abs_path = os.path.join(self.test_dir, "src", "config.json")
        mock_join.return_value = abs_path
        
        # Make sure os.path.exists returns True for our test file
        mock_exists.return_value = True
        
        # Create a mock for engine.scan_file to return our expected findings
        expected_findings = [
            {
                "rule_id": "sensitive_variable_names",
                "rule_name": "Sensitive Variable Names",
                "severity": "medium",
                "type": "variable_name_match",
                "variable": "password",
                "value": "super_secret_password",
                "line": 3,
                "path": abs_path,
                "description": "Potential credential in variable 'password'"
            },
            {
                "rule_id": "sensitive_variable_names",
                "rule_name": "Sensitive Variable Names",
                "severity": "medium",
                "type": "variable_name_match",
                "variable": "apiKey",
                "value": "api_key_1234567890abcdef",
                "line": 2,
                "path": abs_path,
                "description": "Potential credential in variable 'apiKey'"
            }
        ]
        
        # Patch the scan_file method to return our expected findings
        with patch('credscan.core.engine.ScanEngine.scan_file', return_value=expected_findings):
            # Run the test
            scanner = PreCommitScanner(self.config)
            findings = scanner.scan_staged_files()
        
        # Verify that findings are returned
        self.assertTrue(len(findings) > 0, "No findings returned")
        
        # Check that we found the credentials in the test file
        found_password = False
        found_api_key = False
        
        for finding in findings:
            if "password" in finding.get("variable", "").lower() and "super_secret_password" in finding.get("value", ""):
                found_password = True
            elif "apikey" in finding.get("variable", "").lower() and "api_key_1234567890abcdef" in finding.get("value", ""):
                found_api_key = True
        
        self.assertTrue(found_password, "Password credential not found")
        self.assertTrue(found_api_key, "API key credential not found")
    
    @patch('subprocess.run')
    @patch('os.makedirs')
    @patch('os.path.exists')
    @patch('builtins.open')
    @patch('os.chmod')
    def test_install_hook(self, mock_chmod, mock_open, mock_exists, mock_makedirs, mock_run):
        """Test installing the pre-commit hook."""
        # Setup mocks
        process_mock = MagicMock()
        process_mock.stdout = "/path/to/repo\n"
        mock_run.return_value = process_mock
        
        mock_exists.return_value = False
        
        # Run the test
        result = install_hook()
        
        # Verify
        self.assertTrue(result)
        mock_run.assert_called()
        mock_makedirs.assert_called_once()
        mock_open.assert_called_once()
        mock_chmod.assert_called_once()
    
    @patch('subprocess.run')
    @patch('os.makedirs')
    @patch('os.path.exists')
    @patch('builtins.open')
    @patch('os.rename')
    @patch('os.chmod')
    def test_install_hook_with_existing_hook(self, mock_chmod, mock_rename, mock_open, mock_exists, mock_makedirs, mock_run):
        """Test installing the pre-commit hook when one already exists."""
        # Setup mocks
        process_mock = MagicMock()
        process_mock.stdout = "/path/to/repo\n"
        mock_run.return_value = process_mock
        
        mock_exists.return_value = True
        
        # Mock file read to return content that doesn't contain our hook
        mock_file = MagicMock()
        mock_file.__enter__.return_value.read.return_value = "#!/bin/sh\necho 'Some existing hook'\n"
        mock_open.return_value = mock_file
        
        # Run the test
        result = install_hook()
        
        # Verify
        self.assertTrue(result)
        mock_run.assert_called()
        mock_makedirs.assert_called_once()
        mock_rename.assert_called_once()  # Should backup existing hook
        self.assertEqual(mock_open.call_count, 2)  # Once to read, once to write
        mock_chmod.assert_called_once()

if __name__ == "__main__":
    unittest.main()