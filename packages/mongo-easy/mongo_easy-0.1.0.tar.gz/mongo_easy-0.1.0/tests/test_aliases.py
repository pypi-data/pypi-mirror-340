import unittest
from mongo_easy.aliasing.registry import get_alias
from mongo_easy.core.connection import connect, get_db

class TestAliases(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        connect(db_name="test_db")
        cls.collection = "test_users"
        cls.db = get_db()

    def test_alias(self):
        add_user = get_alias("add_user")
        add_user({"name": "Charlie", "age": 29})
        result = self.db[self.collection].find({"name": "Charlie"})
        self.assertEqual(result.count(), 1)

if __name__ == "__main__":
    unittest.main()
