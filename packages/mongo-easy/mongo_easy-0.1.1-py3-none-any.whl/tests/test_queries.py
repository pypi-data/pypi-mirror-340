import unittest
from mongo_easy.core.connection import connect, get_db
from mongo_easy.core.queries import find_sorted, count

class TestQueries(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        connect(db_name="test_db")
        cls.collection = "test_users"
        cls.db = get_db()

    def test_find_sorted(self):
        users = [{"name": "Bob", "age": 25}, {"name": "Alice", "age": 30}]
        self.db[self.collection].insert_many(users)

        sorted_users = find_sorted(self.collection, sort_by="age", direction=-1)
        self.assertEqual(sorted_users[0]["name"], "Alice")
        self.assertEqual(sorted_users[1]["name"], "Bob")

    def test_count(self):
        user_count = count(self.collection)
        self.assertGreater(user_count, 0)

if __name__ == "__main__":
    unittest.main()
