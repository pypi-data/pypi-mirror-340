# Mongo Easy 🧠🍃

**Mongo Easy** is a beginner-friendly Python library that makes working with MongoDB super simple and readable — even for non-coders. Whether you're building a script, a CLI tool, or just learning databases, Mongo Easy helps you do CRUD operations with minimal setup and code.

---

## 🔥 Features

- ⚡ One-line `connect()` to MongoDB
- 📁 Simple `save()`, `find()`, `update()`, and `delete()` functions
- 🧰 Optional collection aliases (`alias("users", "u")`)
- 🧪 Easy-to-read code — perfect for learners or quick scripting
- 💻 Built-in CLI to run MongoDB operations from your terminal
- 📤 CSV/JSON import/export
- 🧪 Test suite included
- 🧩 Custom utils for common DB tasks

---

## 🚀 Installation

```bash
pip install mongo-easy
```

Or clone for development:

```bash
git clone https://github.com/prakhardoneria/mongo_easy.git
cd mongo_easy
pip install -e .
```

---

## 🛠️ Quick Start

```python
from mongo_easy.core.connection import connect
from mongo_easy.core.crud import save, find

connect()  # connect to local MongoDB

# Insert a document
save("users", {"name": "Alice", "age": 30})

# Query documents
users = find("users", {"age": {"$gte": 18}})
print(users)
```

---

## 🧪 CLI Usage

```bash
# List all collections
mongo-easy list

# Insert a user
mongo-easy insert users --data '{"name": "Bob", "age": 25}'

# Find users
mongo-easy find users --filter '{"age": {"$gt": 20}}'
```

---

## 🧩 Modules

- `core`: Core CRUD operations + MongoDB connection
- `cli`: Command-line interface helpers
- `io`: CSV/JSON import/export
- `aliasing`: Define shortcuts for collection names
- `utils`: Common utility functions for MongoDB operations

---

## 🧰 Example

```python
from mongo_easy import connect, save, find

connect("mongodb://localhost:27017", db_name="school")

save("students", {"name": "John", "grade": "A"})
students = find("students", {"grade": "A"})

for s in students:
    print(s)
```

---

## 📁 Project Structure

```
mongo_easy/
├── core/
├── cli/
├── io/
├── aliasing/
├── utils/
├── tests/
├── examples/
└── docs/
```

---

## 📄 Docs

- [Getting Started](docs/getting_started.md)
- [Function Reference](docs/functions_reference.md)
- [CLI Guide](docs/cli_guide.md)
- [FAQ](docs/faq.md)

---

## 🧪 Testing

```bash
pytest
```

Use `mongomock` for offline tests (optional).

---

## 🤝 Contributing

Pull requests are welcome! Check out the [Contributing Guide](CONTRIBUTING.md) (or create one!) to get started.

---

## 📝 License

MIT License. Use it freely and star it if you love it ⭐

---

## 🙌 Author

Made with ❤️ by [Prakhar Doneria](https://github.com/prakhardoneria)