# 🔗 URL Shortener Service

A simple and convenient URL shortening service with Docker support and a test environment.

---

## 🚀 Quick Start with Docker

Follow these steps to run the project locally:

### 1. Clone the repository

```bash
cd <your preferred directory>
git clone https://github.com/kotyra911/shortener-service.git
````

### 2. Create environment files

In the project root, create `.env` and `.test.env` files based on the example:

```bash
.env.example
```

Note that the test database name should be the same as the main one, but with the **_test** prefix.

---

## ▶️ Running the Project

Build and start the service:

```bash
docker compose up --build
```

To stop the process:

```bash
Ctrl + C
```

---

## 🧪 Running Tests

To run tests, use:

```bash
docker compose run --rm web pytest
```

---

## ⛔ Stopping Containers

To completely stop and remove containers:

```bash
docker compose down
```

---

## 📌 Description

This service provides an API for shortening long URLs.
It allows you to generate short links and redirect users to the original addresses.

---

## 💡 Features

* Create short links
* Redirect to the original URL
* Track the number of clicks for each link
* Docker support
* Separate test environment
* Easy scalability

---

## 🛠️ Tech Stack

* Python
* FastAPI
* PostgreSQL
* Docker
* Pytest

---
