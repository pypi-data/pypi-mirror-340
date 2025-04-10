"""
Tests for the detection rules system.
"""
import unittest
from credscan.detection import Rule, RuleLoader

class TestRule(unittest.TestCase):
    """Test the Rule class functionality."""
    
    def test_rule_initialization(self):
        """Test that a rule can be initialized from a configuration."""
        rule_config = {
            "id": "test_rule",
            "name": "Test Rule",
            "description": "A rule for testing",
            "severity": "high",
            "variable_patterns": [
                r"(?i)password",
                r"(?i)secret"
            ],
            "value_patterns": [
                {
                    "name": "Test Pattern",
                    "pattern": r"test-\d+"
                }
            ],
            "min_length": 5
        }
        
        rule = Rule(rule_config)
        
        self.assertEqual(rule.id, "test_rule")
        self.assertEqual(rule.name, "Test Rule")
        self.assertEqual(rule.description, "A rule for testing")
        self.assertEqual(rule.severity, "high")
        self.assertEqual(rule.min_length, 5)
        self.assertEqual(len(rule.variable_patterns), 2)
        self.assertEqual(len(rule.value_patterns), 1)
    
    def test_variable_name_match(self):
        """Test matching variable names against patterns."""
        rule_config = {
            "id": "test_rule",
            "variable_patterns": [
                r"(?i)password",
                r"(?i)secret",
                r"(?i)token"
            ],
            "variable_exclusion_pattern": r"(?i)test|dummy"
        }
        
        rule = Rule(rule_config)
        
        # Test positive matches
        self.assertTrue(rule.is_variable_name_match("password"))
        self.assertTrue(rule.is_variable_name_match("PASSWORD"))
        self.assertTrue(rule.is_variable_name_match("userSecret"))
        self.assertTrue(rule.is_variable_name_match("api_token"))
        
        # Test negative matches
        self.assertFalse(rule.is_variable_name_match("username"))
        self.assertFalse(rule.is_variable_name_match("email"))
        
        # Test exclusion pattern
        self.assertFalse(rule.is_variable_name_match("test_password"))
        self.assertFalse(rule.is_variable_name_match("dummy_token"))
    
    def test_value_pattern_match(self):
        """Test matching values against patterns."""
        rule_config = {
            "id": "test_rule",
            "value_patterns": [
                {
                    "name": "JWT Token",
                    "pattern": r"eyJhbGciOiJIUzI1NiIsInR5cCI[a-zA-Z0-9_.]+"
                },
                {
                    "name": "API Key",
                    "pattern": r"api_key_[a-zA-Z0-9]{16}"
                }
            ],
            "min_length": 10
        }
        
        rule = Rule(rule_config)
        
        # Test positive matches
        jwt_match = rule.get_value_pattern_match("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0")
        self.assertIsNotNone(jwt_match)
        self.assertEqual(jwt_match["pattern_name"], "JWT Token")
        
        api_key_match = rule.get_value_pattern_match("api_key_1234567890abcdef")
        self.assertIsNotNone(api_key_match)
        self.assertEqual(api_key_match["pattern_name"], "API Key")
        
        # Test negative matches
        self.assertIsNone(rule.get_value_pattern_match("not_a_match"))
        self.assertIsNone(rule.get_value_pattern_match("api_key_short"))
        
        # Test value too short
        self.assertIsNone(rule.get_value_pattern_match("short"))
    
    def test_apply_rule(self):
        """Test applying a rule to parsed content."""
        rule_config = {
            "id": "test_rule",
            "name": "Test Rule",
            "severity": "medium",
            "variable_patterns": [
                r"(?i)password",
                r"(?i)secret"
            ],
            "value_patterns": [
                {
                    "name": "JWT Token",
                    "pattern": r"eyJhbGciOiJIUzI1NiIsInR5cCI[a-zA-Z0-9_.]+"
                }
            ],
            "min_length": 5
        }
        
        rule = Rule(rule_config)
        
        # Create some parsed content with potential findings
        parsed_content = {
            "type": "json",
            "path": "test.json",
            "items": [
                {
                    "key": "username",
                    "value": "john",
                    "line": 1,
                    "type": "property"
                },
                {
                    "key": "password",
                    "value": "secret123",
                    "line": 2,
                    "type": "property"
                },
                {
                    "key": "token",
                    "value": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0",
                    "line": 3,
                    "type": "property"
                }
            ]
        }
        
        findings = rule.apply(parsed_content, "test.json")
        
        # Should find 2 issues: password variable and JWT token
        self.assertEqual(len(findings), 2)
        
        # Check the password finding
        password_finding = next((f for f in findings if f["variable"] == "password"), None)
        self.assertIsNotNone(password_finding)
        self.assertEqual(password_finding["rule_id"], "test_rule")
        self.assertEqual(password_finding["severity"], "medium")
        self.assertEqual(password_finding["type"], "variable_name_match")
        self.assertEqual(password_finding["line"], 2)
        
        # Check the JWT token finding
        jwt_finding = next((f for f in findings if f["variable"] == "token"), None)
        self.assertIsNotNone(jwt_finding)
        self.assertEqual(jwt_finding["rule_id"], "test_rule")
        self.assertEqual(jwt_finding["severity"], "medium")
        self.assertEqual(jwt_finding["type"], "value_pattern_match")
        self.assertEqual(jwt_finding["pattern"], "JWT Token")
        self.assertEqual(jwt_finding["line"], 3)


class TestRuleLoader(unittest.TestCase):
    """Test the RuleLoader class functionality."""
    
    def test_load_default_rules(self):
        """Test loading the default rules."""
        rules = RuleLoader.load_default_rules()
        
        # Check that rules were loaded
        self.assertGreater(len(rules), 0)
        
        # Check that rules are properly initialized
        for rule in rules:
            self.assertIsInstance(rule, Rule)
            self.assertTrue(hasattr(rule, 'id'))
            self.assertTrue(hasattr(rule, 'name'))
            self.assertTrue(hasattr(rule, 'severity'))


if __name__ == "__main__":
    unittest.main()
