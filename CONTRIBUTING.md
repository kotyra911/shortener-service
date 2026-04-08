# Contributing to URL Shortener Service

Thank you for your interest in this project! 🎉
Contributions of all kinds are welcome: bug fixes, improvements, and new features.

---

## 🚀 Getting Started

### 1. Fork the repository

Click the **Fork** button and clone your fork:

```
git clone https://github.com/<your-username>/shortener-service.git
cd shortener-service
```

---

### 2. Set up environment

Create `.env` and `.test.env` files based on `.env.example`.

> ⚠️ Important: the test database name should match the main one with a `_test` suffix.

---

### 3. Run the project

```
docker compose up --build
```

---

### 4. Verify everything works

Run tests:

```
docker compose run --rm web pytest
```

---

## 🛠️ Making Changes

### 1. Create a branch

For features:

```
git checkout -b feature/your-feature-name
```

For bug fixes:

```
git checkout -b fix/bug-description
```

---

### 2. Make your changes

* Follow the existing code style
* Use clear and descriptive names
* Add comments if the logic is complex

---

### 3. Add tests (if needed)

If you:

* add a new feature → include tests
* fix a bug → add a test that covers it

---

### 4. Run tests

```
docker compose run --rm web pytest
```

---

### 5. Commit your changes

Use clear commit messages:

```
feat: add URL expiration feature
fix: correct redirect logic
docs: update README
```

---

### 6. Open a Pull Request

* Describe what you did
* Link related issues (if any)
* Add steps to test your changes

---

## 🐞 Reporting Bugs

If you find a bug:

1. Check if it already exists in issues
2. If not, create a new issue and include:

   * what happened
   * expected behavior
   * steps to reproduce

---

## 💡 Feature Requests

Want to suggest an idea?

* Open an issue
* Clearly explain the use case and benefit

---

## 🏷️ Issues for Contributors

Look for issues labeled:

* `good first issue` — great for beginners
* `help wanted` — contributions needed

---

## 📏 Code Style

* Follow PEP 8
* Write clean and readable code
* Keep functions small and focused

---

## 🤝 Communication

* Be respectful and constructive
* Ask questions if something is unclear

---

## ❤️ Thank You

Every contribution helps improve the project. Thank you for being part of it!
