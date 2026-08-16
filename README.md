# Inventory Management System

A Flask-based REST API for managing retail inventory, with integration to the
[OpenFoodFacts API](https://world.openfoodfacts.org/) for enriching product
data, plus a CLI client for interacting with the API.

## Features

- Full CRUD REST API for inventory items (`GET`, `POST`, `PATCH`, `DELETE`)
- Lookup products on OpenFoodFacts by barcode or by name
- Add an OpenFoodFacts product straight into inventory by barcode
- CLI tool to drive the API interactively
- JSON-file-backed storage simulating a database
- Unit tests for routes, the external API client, and the CLI (with mocked
  HTTP calls)

## Project Structure

```
inventory-management-system/
├── data/
│   └── inventory.json        # simulated database (array of items)
├── src/
│   ├── app.py                 # Flask app factory / entrypoint
│   ├── cli.py                 # CLI frontend
│   ├── models/
│   │   └── inventory.py       # data access layer (JSON file storage)
│   ├── routes/
│   │   └── inventory_routes.py  # Flask blueprint / REST endpoints
│   └── services/
│       └── openfoodfacts.py   # OpenFoodFacts API client
├── tests/
│   ├── conftest.py
│   ├── test_inventory_routes.py
│   ├── test_openfoodfacts_service.py
│   └── test_cli.py
└── requirements.txt
```

## Setup

1. Clone the repository and move into the project directory.
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the Flask API (defaults to `http://127.0.0.1:5000`):
   ```bash
   python -m src.app
   ```
5. In a second terminal (with the venv activated), run the CLI:
   ```bash
   python -m src.cli
   ```

## API Endpoints

| Method | Endpoint                                     | Description                                        |
|--------|-----------------------------------------------|----------------------------------------------------|
| GET    | `/inventory`                                  | Fetch all inventory items                          |
| GET    | `/inventory/<id>`                             | Fetch a single item by ID                           |
| POST   | `/inventory`                                  | Add a new item                                      |
| PATCH  | `/inventory/<id>`                             | Update an existing item                              |
| DELETE | `/inventory/<id>`                             | Remove an item                                       |
| GET    | `/inventory/lookup/barcode/<barcode>`         | Look up a product on OpenFoodFacts by barcode        |
| GET    | `/inventory/lookup/search?name=<query>`       | Search products on OpenFoodFacts by name             |
| POST   | `/inventory/lookup/barcode/<barcode>/add`     | Look up a product by barcode and add it to inventory |

### Example: create an item

```bash
curl -X POST http://127.0.0.1:5000/inventory \
  -H "Content-Type: application/json" \
  -d '{"product_name": "Organic Almond Milk", "brands": "Silk", "price": 3.99, "quantity": 10}'
```

### Example: update stock

```bash
curl -X PATCH http://127.0.0.1:5000/inventory/1 \
  -H "Content-Type: application/json" \
  -d '{"quantity": 25}'
```

### Example: add a product from OpenFoodFacts by barcode

```bash
curl -X POST http://127.0.0.1:5000/inventory/lookup/barcode/3017620422003/add \
  -H "Content-Type: application/json" \
  -d '{"price": 4.5, "quantity": 8}'
```

## Data Model

Each inventory item is stored as an object such as:

```json
{
  "id": 1,
  "product_name": "Organic Almond Milk",
  "brands": "Silk",
  "barcode": "3017620422003",
  "ingredients_text": "Filtered water, almonds, cane sugar",
  "price": 3.99,
  "quantity": 10
}
```

## CLI Usage

Run `python -m src.cli` while the Flask server is running, then choose from
the menu:

```
1. View all inventory
2. View item by ID
3. Add new item
4. Update item price/quantity
5. Delete item
6. Find item on OpenFoodFacts (by barcode)
7. Find item on OpenFoodFacts (by name)
8. Add item from OpenFoodFacts barcode lookup
0. Exit
```

The CLI handles invalid numeric input and reports API/network errors instead
of crashing.

## Testing

Run the full test suite with:

```bash
python -m pytest tests/ -v
```

Tests cover:
- API endpoints (GET, POST, PATCH, DELETE, including error cases)
- The OpenFoodFacts client (mocked with `unittest.mock`, including network
  failure handling)
- CLI commands (mocked HTTP requests and stdin)
