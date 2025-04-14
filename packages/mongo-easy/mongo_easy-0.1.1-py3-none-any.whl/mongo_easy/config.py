import unittest
from mongo_easy.core.connection import connect, get_db
from mongo_easy.core.crud import save, find, delete
from bson import ObjectId

class TestCRUDOperations(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        connect(db_name="test_db")
        cls.collection = "test_users"
        cls.db = get_db()

    def test_save_and_find(self):
        # Test inserting and finding data
        user_data = {"name": "Alice", "age": 30}
        save(self.collection, user_data)

        result = find(self.collection, {"name": "Alice"})
        self.assertGreater(len(result), 0)
        self.assertEqual(result[0]["name"], "Alice")

    def test_delete(self):
        # Test deleting data
        delete(self.collection, {"name": "Alice"})
        result = find(self.collection, {"name": "Alice"})
        self.assertEqual(len(result), 0)

if __name__ == "__main__":
    unittest.main()
