"""
Tests for the git history scanning functionality.
"""
import os
import tempfile
import unittest
import subprocess
from unittest.mock import patch, MagicMock, call
import datetime

from credscan.history.scanner import HistoryScanner
from credscan.history.commit_analyzer import CommitAnalyzer
from credscan.history.diff_processor import DiffProcessor
from credscan.history.result_manager import HistoryResultManager

class TestHistoryScanner(unittest.TestCase):
    """Test git history scanning functionality."""
    
    def setUp(self):
        """Set up the test environment."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_dir = self.temp_dir.name
        
        # Create a test git repository
        self.create_test_repo()
        
        # Default config
        self.config = {
            'verbose': True
        }
    
    def tearDown(self):
        """Clean up the test environment."""
        self.temp_dir.cleanup()
    
    def create_test_repo(self):
        """Create a test git repository with history."""
        # Initialize a git repository
        os.chdir(self.test_dir)
        subprocess.run(["git", "init"], check=True)
        subprocess.run(["git", "config", "user.name", "Test User"], check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], check=True)
        
        # Create initial files without credentials
        os.makedirs("src", exist_ok=True)
        with open("src/config.py", "w") as f:
            f.write("# Initial config\nDEBUG = True\n")
        
        # First commit
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "Initial commit"], check=True)
        
        # Second commit - add a credential
        with open("src/config.py", "w") as f:
            f.write("# Config with API key\nDEBUG = True\nAPI_KEY = 'test_secret_12345'\n")
        
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "Add API key"], check=True)
        
        # Third commit - remove credential
        with open("src/config.py", "w") as f:
            f.write("# Config without API key\nDEBUG = True\n")
        
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "Remove API key"], check=True)
        
        # Change back to original dir
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    @patch('subprocess.run')
    def test_get_commit_list(self, mock_run):
        """Test getting the commit list."""
        # Setup mock
        process_mock = MagicMock()
        process_mock.stdout = "commit1\ncommit2\ncommit3\n"
        mock_run.return_value = process_mock
        
        # Run the test
        with patch('credscan.history.scanner.HistoryScanner._get_repo_root', return_value=self.test_dir):
            scanner = HistoryScanner(self.config)
            commits = scanner._get_commit_list()
        
        # Verify
        self.assertEqual(commits, ["commit1", "commit2", "commit3"])
        mock_run.assert_called()
    
    @patch('credscan.history.scanner.HistoryScanner._get_commit_list')
    @patch('credscan.history.commit_analyzer.CommitAnalyzer.analyze_commit')
    def test_scan(self, mock_analyze, mock_get_commits):
        """Test scanning git history."""
        # Setup mocks
        mock_get_commits.return_value = ["commit1", "commit2"]
        
        # Mock findings from each commit
        mock_analyze.side_effect = [
            [{"value": "secret1", "commit_hash": "commit1"}],
            [{"value": "secret2", "commit_hash": "commit2"}]
        ]
        
        # Run the test
        with patch('credscan.history.scanner.HistoryScanner._get_repo_root', return_value=self.test_dir):
            scanner = HistoryScanner(self.config)
            findings = scanner.scan()
        
        # Verify
        self.assertEqual(len(findings), 2)
        mock_get_commits.assert_called_once()
        self.assertEqual(mock_analyze.call_count, 2)

class TestCommitAnalyzer(unittest.TestCase):
    """Test the CommitAnalyzer class."""
    
    def setUp(self):
        """Set up the test environment."""
        self.config = {'verbose': True}
        
    @patch('subprocess.run')
    def test_get_commit_info(self, mock_run):
        """Test getting commit information."""
        # Setup mock
        process_mock = MagicMock()
        process_mock.stdout = "abc123\nTest User\ntest@example.com\n1617184000\nTest commit"
        mock_run.return_value = process_mock
        
        # Run the test
        analyzer = CommitAnalyzer(self.config)
        info = analyzer.get_commit_info("abc123")
        
        # Verify
        self.assertEqual(info["hash"], "abc123")
        self.assertEqual(info["author_name"], "Test User")
        self.assertEqual(info["timestamp"], 1617184000)
        mock_run.assert_called_once()
    
    @patch('subprocess.run')
    def test_get_changed_files(self, mock_run):
        """Test getting changed files in a commit."""
        # Setup mock
        process_mock = MagicMock()
        process_mock.stdout = "A\tsrc/new_file.py\nM\tsrc/modified_file.py\nD\tsrc/deleted_file.py"
        mock_run.return_value = process_mock
        
        # Run the test
        analyzer = CommitAnalyzer(self.config)
        files = analyzer.get_changed_files("abc123")
        
        # Verify
        self.assertEqual(len(files), 3)
        self.assertIn(("src/new_file.py", "A"), files)
        self.assertIn(("src/modified_file.py", "M"), files)
        self.assertIn(("src/deleted_file.py", "D"), files)
        mock_run.assert_called_once()
    
    @patch('credscan.history.commit_analyzer.CommitAnalyzer.get_commit_info')
    @patch('credscan.history.commit_analyzer.CommitAnalyzer.get_changed_files')
    @patch('credscan.history.commit_analyzer.CommitAnalyzer.is_binary_file')
    @patch('credscan.history.diff_processor.DiffProcessor.process_file_diff')
    def test_analyze_commit(self, mock_process_diff, mock_is_binary, mock_get_files, mock_get_info):
        """Test analyzing a commit."""
        # Setup mocks
        mock_get_info.return_value = {
            "hash": "abc123",
            "author_name": "Test User",
            "timestamp": 1617184000,
            "message": "Test commit"
        }
        mock_get_files.return_value = [
            ("src/file1.py", "A"),
            ("src/file2.py", "M"),
            ("src/file3.py", "D")  # Deleted file, should be skipped
        ]
        mock_is_binary.return_value = False
        
        # Mock the diff processing to return findings for one file
        mock_process_diff.side_effect = [
            [{"value": "secret1", "path": "src/file1.py"}],
            []  # No findings in second file
        ]
        
        # Run the test
        analyzer = CommitAnalyzer(self.config)
        findings = analyzer.analyze_commit("abc123")
        
        # Verify
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]["value"], "secret1")
        self.assertEqual(findings[0]["commit_hash"], "abc123")
        self.assertEqual(findings[0]["commit_author"], "Test User")
        
        # Should process only 2 files (not the deleted one)
        self.assertEqual(mock_process_diff.call_count, 2)

class TestResultManager(unittest.TestCase):
    """Test the HistoryResultManager class."""
    
    def test_process_commit_findings(self):
        """Test processing and deduplicating findings."""
        manager = HistoryResultManager()
        
        # First set of findings
        findings1 = [
            {"rule_id": "rule1", "original_file": "file1.py", "variable": "var1", "value": "secret1"},
            {"rule_id": "rule2", "original_file": "file2.py", "variable": "var2", "value": "secret2"}
        ]
        
        # Process first set
        unique1 = manager.process_commit_findings("commit1", findings1)
        
        # Should have 2 unique findings
        self.assertEqual(len(unique1), 2)
        self.assertEqual(len(manager.findings), 2)
        
        # Second set with one duplicate and one new
        findings2 = [
            {"rule_id": "rule1", "original_file": "file1.py", "variable": "var1", "value": "secret1"},  # Duplicate
            {"rule_id": "rule3", "original_file": "file3.py", "variable": "var3", "value": "secret3"}   # New
        ]
        
        # Process second set
        unique2 = manager.process_commit_findings("commit2", findings2)
        
        # Should have 1 unique finding
        self.assertEqual(len(unique2), 1)
        self.assertEqual(len(manager.findings), 3)
        
        # Get all findings
        all_findings = manager.get_findings()
        self.assertEqual(len(all_findings), 3)

# Main test function
if __name__ == "__main__":
    unittest.main()