# Matrix Utils

[![PyPI](https://img.shields.io/pypi/v/matrix-utils)](https://pypi.org/project/matrix-utils)
[![Python](https://img.shields.io/pypi/pyversions/matrix-utils)](https://pypi.org/project/matrix-utils)
[![License](https://img.shields.io/pypi/l/matrix-utils)](LICENSE)

**Matrix Utils** is a lightweight Python library for creating and working with structured matrices.  
It supports identity, tri-diagonal, tri-band, diagonal, symmetric, Toeplitz, Hankel, and circulant matrices — all in a clean object-oriented style.

---

## ✨ Features

- Object-oriented `Matrix` class
- Add, multiply, and transpose matrices
- Generate:
  - Identity matrix
  - Diagonal, symmetric
  - Tri-diagonal, tri-band
  - Toeplitz, Hankel, Circulant
- Utility functions:
  - Check for symmetry
  - Check for Toeplitz

---

## 📦 Installation

```bash
pip install matrixx
```

---

## 🚀 Usage

```python
from matrix_utils import Matrix, generate_tridiagonal, is_toeplitz

m = generate_tridiagonal(4)
print(m)

print(m.transpose())
print(m.is_symmetric())

print(is_toeplitz(m))
```

---

## 📂 Project Structure

```
matrix-utils/
├── matrix_utils/
│   ├── core.py
│   └── __init__.py
├── tests/
├── setup.py
├── LICENSE
└── README.md
```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).  
© 2024 Kranthi • Contact: [kdevprofile@gmail.com](mailto:kdevprofile@gmail.com)
