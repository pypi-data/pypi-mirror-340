# Moroccan Atlas

A Python toolbox of validators, parsers, and datasets for Moroccan-specific data formats and regions.

> **Note:** This project is **under heavy development**. Features and functionality may and will change over time.

## Installation

```bash
pip install moroccan_atlas
```

## Usage

```python
from moroccan_atlas import is_valid_cin, is_valid_ice, is_valid_phone

print(is_valid_cin("AB123456"))          # True
print(is_valid_ice("001234567000084"))   # True
print(is_valid_phone("0600123456"))      # True
```

## Validators Available

is_valid_XYZ, return True or False

- `is_valid_cin(value)` — 8-character alphanumeric CIN, must start with letters.
<!-- - `is_valid_ice(value)` — 15-digit ICE (business identifier).
- `is_valid_phone(value)` — Validates Moroccan mobile phone numbers. -->

## Extractors

Do not perform validation. Just extract data directly.

## Parsers

Parsers perform validation + extraction of data.
If it's invalid, they raise a ValidationError exception.


## Data

Compressed CSVs or JSONs

Load with importlib.resources (modern & zip-safe way)

Check size of package:
    python -m build
    du -sh dist/*

## License

> A commercial license is required for any organization with more than 10 employees or annual revenue over $500,000 USD, or using this software as part of a product or service offered for a fee.

See LICENSE, or contact the author, for more details.
