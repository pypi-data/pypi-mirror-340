"""
Tests for the file parsers.
"""
import os
import tempfile
import unittest
from credscan.parsers import JSONParser, YAMLParser, CodeParser

class TestJSONParser(unittest.TestCase):
    """Test the JSON parser functionality."""
    
    def setUp(self):
        """Set up the test environment."""
        self.parser = JSONParser()
        self.temp_dir = tempfile.TemporaryDirectory()
    
    def tearDown(self):
        """Clean up the test environment."""
        self.temp_dir.cleanup()
    
    def create_test_file(self, content):
        """Create a temporary test file with the given content."""
        file_path = os.path.join(self.temp_dir.name, "test.json")
        with open(file_path, "w") as f:
            f.write(content)
        return file_path
    
    def test_can_parse(self):
        """Test that the parser correctly identifies JSON files."""
        self.assertTrue(self.parser.can_parse("file.json"))
        self.assertFalse(self.parser.can_parse("file.yaml"))
        self.assertFalse(self.parser.can_parse("file.txt"))
    
    def test_parse_empty_file(self):
        """Test parsing an empty file."""
        file_path = self.create_test_file("")
        result = self.parser.parse(file_path)
        self.assertIsNotNone(result)
        self.assertIn("error", result)
        self.assertEqual(result["type"], "json")
    
    def test_parse_valid_json(self):
        """Test parsing a valid JSON file."""
        json_content = """
        {
            "apiKey": "some-api-key-12345",
            "config": {
                "password": "secretpassword"
            },
            "items": ["a", "b", "c"]
        }
        """
        file_path = self.create_test_file(json_content)
        result = self.parser.parse(file_path)
        
        self.assertIsNotNone(result)
        self.assertIsNone(result["error"])
        self.assertEqual(result["type"], "json")
        
        # Check that the parser extracted the items correctly
        items = result["items"]
        self.assertEqual(len(items), 5)  # apiKey, config, password, and 3 list items
        
        # Check specific items
        api_key_item = next((item for item in items if item["key"] == "apiKey"), None)
        self.assertIsNotNone(api_key_item)
        self.assertEqual(api_key_item["value"], "some-api-key-12345")
        
        password_item = next((item for item in items if item["key"] == "password"), None)
        self.assertIsNotNone(password_item)
        self.assertEqual(password_item["value"], "secretpassword")
    
    def test_parse_invalid_json(self):
        """Test parsing an invalid JSON file."""
        json_content = "{ This is not valid JSON }"
        file_path = self.create_test_file(json_content)
        result = self.parser.parse(file_path)
        
        self.assertIsNotNone(result)
        self.assertIn("error", result)
        self.assertIsNotNone(result["error"])
        self.assertEqual(result["type"], "json")


class TestYAMLParser(unittest.TestCase):
    """Test the YAML parser functionality."""
    
    def setUp(self):
        """Set up the test environment."""
        self.parser = YAMLParser()
        self.temp_dir = tempfile.TemporaryDirectory()
    
    def tearDown(self):
        """Clean up the test environment."""
        self.temp_dir.cleanup()
    
    def create_test_file(self, content):
        """Create a temporary test file with the given content."""
        file_path = os.path.join(self.temp_dir.name, "test.yaml")
        with open(file_path, "w") as f:
            f.write(content)
        return file_path
    
    def test_can_parse(self):
        """Test that the parser correctly identifies YAML files."""
        self.assertTrue(self.parser.can_parse("file.yaml"))
        self.assertTrue(self.parser.can_parse("file.yml"))
        self.assertFalse(self.parser.can_parse("file.json"))
        self.assertFalse(self.parser.can_parse("file.txt"))
    
    def test_parse_valid_yaml(self):
        """Test parsing a valid YAML file."""
        yaml_content = """
        apiKey: some-api-key-12345
        config:
        password: secretpassword
        items:
        - a
        - b
        - c
        """
        file_path = self.create_test_file(yaml_content)
        result = self.parser.parse(file_path)
        
        self.assertIsNotNone(result)
        self.assertIsNone(result["error"])
        self.assertEqual(result["type"], "yaml")
        
        # Check that the parser extracted the items correctly
        items = result["items"]
        self.assertEqual(len(items), 5)  # apiKey, config, password, and 3 list items
        
        # Check specific items
        api_key_item = next((item for item in items if item["key"] == "apiKey"), None)
        self.assertIsNotNone(api_key_item)
        self.assertEqual(api_key_item["value"], "some-api-key-12345")
        
        password_item = next((item for item in items if item["key"] == "password"), None)
        self.assertIsNotNone(password_item)
        self.assertEqual(password_item["value"], "secretpassword")


class TestCodeParser(unittest.TestCase):
    """Test the Code parser functionality."""
    
    def setUp(self):
        """Set up the test environment."""
        self.parser = CodeParser()
        self.temp_dir = tempfile.TemporaryDirectory()
    
    def tearDown(self):
        """Clean up the test environment."""
        self.temp_dir.cleanup()
    
    def create_test_file(self, content, extension=".py"):
        """Create a temporary test file with the given content."""
        file_path = os.path.join(self.temp_dir.name, f"test{extension}")
        with open(file_path, "w") as f:
            f.write(content)
        return file_path
    
    def test_can_parse(self):
        """Test that the parser correctly identifies supported code files."""
        self.assertTrue(self.parser.can_parse("file.py"))
        self.assertTrue(self.parser.can_parse("file.js"))
        self.assertTrue(self.parser.can_parse("file.java"))
        self.assertFalse(self.parser.can_parse("file.json"))
        self.assertFalse(self.parser.can_parse("file.txt"))
    
    def test_parse_python_code(self):
        """Test parsing Python code with variables and comments."""
        python_code = """
        # This is a comment
        API_KEY = "some-api-key-12345"
        
        def get_password():
            # Function to get password
            password = "secretpassword"
            return password
        
        # Multiline comment with sensitive info
        \"\"\"
        Here's a secret token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0
        \"\"\"
        """
        file_path = self.create_test_file(python_code)
        result = self.parser.parse(file_path)
        
        self.assertIsNotNone(result)
        self.assertIsNone(result["error"])
        self.assertEqual(result["type"], "code")
        self.assertEqual(result["language"], "py")
        
        # Check that the parser found variables and comments
        variables = result["variables"]
        comments = result["comments"]
        
        # Check variables
        self.assertTrue(any(v["name"] == "API_KEY" and v["value"] == "some-api-key-12345" for v in variables))
        self.assertTrue(any(v["name"] == "password" and v["value"] == "secretpassword" for v in variables))
        
        # Check comments
        self.assertTrue(any("secret token" in c["text"] for c in comments))

if __name__ == "__main__":
    unittest.main()
