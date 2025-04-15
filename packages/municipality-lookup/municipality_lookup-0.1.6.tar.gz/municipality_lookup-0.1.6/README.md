# 🏛️ Municipality Lookup

**Municipality Lookup** is a lightweight Python library for retrieving information about Italian municipalities, including province, land registry office, national and cadastral codes.

It supports exact and fuzzy search (useful in OCR or typo-prone contexts) and is designed to be fast, cache-friendly and developer-friendly. The official dataset is embedded in the package and automatically loaded.

---

## 📦 Installation

Install via pip:

```bash
pip install municipality-lookup
```

---

## 🚀 Basic usage

Import and initialize the database instance using the built-in CSV:

```python
from municipality_lookup.instance import get_db

# Load the default embedded CSV
db = get_db()
```

### 🔍 Search for a municipality

```python
# Exact match (case-insensitive)
result = db.get_by_name("ABANO TERME")
print(result)
# ➜ Municipality(name='ABANO TERME', province='PD', ...)

# Fuzzy match (handles typos or partial names)
result = db.get_by_name("abno terme")
print(result)
# ➜ Fuzzy match result based on similarity score
```

You can also customize the **minimum similarity score** (default is 0.8):

```python
result = db.get_by_name("abano trm", min_score=0.7)
```

---

### 📋 Get unique values

```python
# List of all provinces
provinces = db.get_all_provinces()
print(sorted(provinces))

# List of all land registry offices
registries = db.get_all_land_registries()
print(sorted(registries))
```

---

### 🔄 Update the internal database with a new CSV

If you have a newer or custom CSV with the same structure, you can load it:

```python
db.update_database("path/to/your_custom_comuni.csv")
```

---

### 📄 CSV structure (for custom data)

If you want to update the internal database using your own CSV, the file must follow this exact structure:

| Column name                      | Description                            |
|----------------------------------|----------------------------------------|
| `Comune`                         | Municipality name (string)             |
| `Provincia`                      | Province code (e.g., "PD")             |
| `Conservatoria di Competenza`   | Land registry office (string)          |
| `Codice Nazionale`              | National municipality code (4-char)    |
| `Codice Catastale`              | Cadastral code (4-char)                |

➡️ The file **must have headers exactly matching these column names** (case sensitive).  
➡️ Missing or malformed rows may be ignored or cause load errors.

✅ Example:

```csv
Comune,Provincia,Conservatoria di Competenza,Codice Nazionale,Codice Catastale
ABANO TERME,PD,Padova,A001,D3AB
ABBADIA CERRETO,LO,Lodi,A004,C1AB
```

---

## 📄 Data source

The dataset used in this library is based on publicly available information provided by:

🔗 [https://www.visurasi.it/elenco-conservatorie-e-comuni](https://www.visurasi.it/elenco-conservatorie-e-comuni)

The data is embedded in the package and can be programmatically updated if needed.

---

## 📜 License

MIT © Andrea Iannazzo