"""
Integration tests for the credential detection system.
"""
import os
import tempfile
import unittest
from credscan.core import ScanEngine
from credscan.parsers import JSONParser, YAMLParser, CodeParser
from credscan.analyzers import EntropyAnalyzer
from credscan.detection import RuleLoader

class TestCredentialScanner(unittest.TestCase):
    """Integration tests for the credential scanner."""
    
    def setUp(self):
        """Set up the test environment."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_files_dir = os.path.join(self.temp_dir.name, "test_files")
        os.makedirs(self.test_files_dir, exist_ok=True)
        
        # Create test files with credentials
        self.create_test_files()
        
        # Configure the scanner
        self.config = {
            'scan_path': self.test_files_dir,
            'verbose': True,
            'max_workers': 2,
            'output_formats': ['console'],
            'enable_entropy': True
        }
        
        # Initialize the scanner
        self.engine = ScanEngine(self.config)
        
        # Register parsers
        self.engine.register_parser(JSONParser(self.config))
        self.engine.register_parser(YAMLParser(self.config))
        self.engine.register_parser(CodeParser(self.config))
        
        # Register analyzers
        self.engine.register_analyzer(EntropyAnalyzer(self.config))
        
        # Add a test-specific rule to detect our test password
        test_rule_config = {
            "id": "test_password_rule",
            "name": "Test Password Rule",
            "description": "Rule for detecting test passwords",
            "severity": "medium",
            "variable_patterns": [
                r"(?i)password"
            ],
            "value_exclusion_patterns": [],  # Don't exclude anything in tests
            "min_length": 5  # Shorter than typical detection
        }
        from credscan.detection import Rule
        test_rule = Rule(test_rule_config)
        
        # Load rules
        rules = RuleLoader.load_default_rules()
        rules.append(test_rule)  # Add our test rule
        self.engine.register_rules(rules)
    
    def tearDown(self):
        """Clean up the test environment."""
        self.temp_dir.cleanup()
    
    def create_test_files(self):
        """Create test files with credentials for scanning."""
        # Create a JSON file with credentials
        json_content = """
        {
            "apiKey": "api_key_1234567890abcdef",
            "password": "super_secret_password",
            "config": {
                "nestedPassword": "another_secret_password"
            },
            "database": {
                "connectionString": "postgres://user:password123@localhost:5432/mydb"
            }
        }
        """
        json_path = os.path.join(self.test_files_dir, "config.json")
        with open(json_path, "w") as f:
            f.write(json_content)
        
        # Create a YAML file with credentials
        yaml_content = """
        secrets:
        api_token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0
        aws_key: AKIAIOSFODNN7EXAMPLE
        
        database:
        username: admin
        password: db_password_123
        """
        yaml_path = os.path.join(self.test_files_dir, "secrets.yaml")
        with open(yaml_path, "w") as f:
            f.write(yaml_content)
        
        # Create a Python file with credentials
        python_content = """
        # Application configuration
        API_KEY = "api_key_9876543210fedcba"
        
        def get_database_config():
            return {
                "user": "admin",
                "password": "super_secure_db_password",
                "host": "db.example.com",
                "port": 5432
            }
        
        # AWS credentials for S3 access
        AWS_ACCESS_KEY = "AKIAXXX7XXXXEXAMPLE"
        AWS_SECRET = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
        """
        python_path = os.path.join(self.test_files_dir, "config.py")
        with open(python_path, "w") as f:
            f.write(python_content)
    
    def test_full_scan(self):
        """Test a full scan of the test directory."""
        # Run the scan
        findings = self.engine.scan()
        
        # Check that the scanner found all test files
        self.assertEqual(self.engine.files_found, 3)
        self.assertEqual(self.engine.files_scanned, 3)
        
        # Check that the scanner found all credentials
        self.assertGreater(len(findings), 0)
        
        # Get all variables and values from findings
        variables = [finding.get("variable", "").lower() for finding in findings]
        values = [finding.get("value", "").lower() for finding in findings]
        
        # Check for key credential types using more flexible checks
        
        # 1. Check for API key
        self.assertTrue(
            any("api" in var for var in variables) or 
            any("api_key" in val for val in values),
            "No API key was found"
        )
        
        # 2. Check for password variables
        self.assertTrue(
            any("password" in var for var in variables),
            "No password variable was found"
        )
        
        # 3. Check for database connection string
        self.assertTrue(
            any("postgres://" in val for val in values),
            "No database connection string was found"
        )
        
        # 4. Check for AWS credentials
        self.assertTrue(
            any("akia" in val for val in values),
            "No AWS key was found"
        )
if __name__ == "__main__":
    unittest.main()
