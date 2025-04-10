# tests/test_baseline.py
import os
import tempfile
import unittest
import json
from credscan.baseline.manager import BaselineManager

class TestBaselineManager(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.baseline_file = os.path.join(self.temp_dir.name, "test-baseline.json")
    
    def tearDown(self):
        self.temp_dir.cleanup()
    
    def test_create_baseline(self):
        manager = BaselineManager(self.baseline_file)
        
        # Add exclusions
        finding = {
            "rule_id": "test_rule",
            "path": "test/file.py",
            "line": 42,
            "value": "test_password_123"
        }
        
        manager.add_finding_exclusion(finding, "Test reason")
        manager.add_pattern_exclusion("TEST_[A-Z0-9]+", "Test pattern")
        manager.add_path_exclusion("test/fixtures/*", "Test fixtures")
        
        # Save baseline
        self.assertTrue(manager.save_baseline())
        
        # Verify file exists
        self.assertTrue(os.path.exists(self.baseline_file))
        
        # Load and verify content
        with open(self.baseline_file, 'r') as f:
            data = json.load(f)
            
        self.assertEqual(data["version"], 1)
        self.assertIn("metadata", data)
        self.assertIn("exclusions", data)
        self.assertEqual(len(data["exclusions"]["findings"]), 1)
        self.assertEqual(len(data["exclusions"]["patterns"]), 1)
        self.assertEqual(len(data["exclusions"]["paths"]), 1)
    
    def test_is_excluded(self):
        manager = BaselineManager(self.baseline_file)
        
        # Add exclusions
        finding1 = {
            "rule_id": "test_rule",
            "path": "test/file.py",
            "line": 42,
            "value": "test_password_123"
        }
        
        finding2 = {
            "rule_id": "other_rule",
            "path": "src/main.py",
            "line": 10,
            "value": "TEST_API_KEY"
        }
        
        finding3 = {
            "rule_id": "another_rule",
            "path": "test/fixtures/config.json",
            "line": 5,
            "value": "some_value"
        }
        
        # Add exclusions
        manager.add_finding_exclusion(finding1, "Test reason")
        manager.add_pattern_exclusion("TEST_[A-Z0-9]+", "Test pattern")
        manager.add_path_exclusion("test/fixtures/*", "Test fixtures")
        
        # Test exact finding match
        result1 = manager.is_excluded(finding1)
        self.assertTrue(result1["excluded"])
        
        # Test pattern match
        result2 = manager.is_excluded(finding2)
        self.assertTrue(result2["excluded"])
        
        # Test path match
        result3 = manager.is_excluded(finding3)
        self.assertTrue(result3["excluded"])
        
        # Test non-match
        result4 = manager.is_excluded({
            "rule_id": "other_rule",
            "path": "src/other.py",
            "line": 20,
            "value": "not_matching"
        })
        self.assertFalse(result4["excluded"])