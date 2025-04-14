import unittest
import json
from mongo_easy.io.csv_handler import import_csv, export_csv
from mongo_easy.core.connection import connect, get_db

class TestIOOperations(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        connect(db_name="test_db")
        cls.collection = "test_users"
        cls.db = get_db()

    def test_export_csv(self):
        # Test exporting to CSV
        export_csv(self.collection, "test_output.csv")
        with open("test_output.csv", "r") as file:
            lines = file.readlines()
        self.assertGreater(len(lines), 0)

    def test_import_csv(self):
        # Test importing from CSV
        import_csv(self.collection, "test_input.csv")
        result = self.db[self.collection].find()
        self.assertGreater(result.count(), 0)

if __name__ == "__main__":
    unittest.main()
