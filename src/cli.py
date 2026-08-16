"""CLI tool for interacting with the Inventory Management System API."""
import requests

API_BASE = "http://127.0.0.1:5000"

MENU = """
=== Inventory Management System ===
1. View all inventory
2. View item by ID
3. Add new item
4. Update item price/quantity
5. Delete item
6. Find item on OpenFoodFacts (by barcode)
7. Find item on OpenFoodFacts (by name)
8. Add item from OpenFoodFacts barcode lookup
0. Exit
"""


def view_all():
    resp = requests.get(f"{API_BASE}/inventory")
    items = resp.json()
    if not items:
        print("No inventory items found.")
        return
    for item in items:
        print(f"[{item['id']}] {item['product_name']} - "
              f"${item.get('price', 0)} - qty: {item.get('quantity', 0)}")


def view_item():
    item_id = input("Enter item ID: ").strip()
    resp = requests.get(f"{API_BASE}/inventory/{item_id}")
    if resp.status_code == 404:
        print("Item not found.")
        return
    print(resp.json())


def add_item():
    product_name = input("Product name: ").strip()
    brands = input("Brand: ").strip()
    barcode = input("Barcode (optional): ").strip()
    price = _prompt_float("Price: ")
    quantity = _prompt_int("Quantity: ")

    payload = {
        "product_name": product_name,
        "brands": brands,
        "barcode": barcode,
        "price": price,
        "quantity": quantity,
    }
    resp = requests.post(f"{API_BASE}/inventory", json=payload)
    if resp.status_code == 201:
        print("Item added:", resp.json())
    else:
        print("Error:", resp.json())


def update_item():
    item_id = input("Enter item ID to update: ").strip()
    price_input = input("New price (leave blank to skip): ").strip()
    quantity_input = input("New quantity (leave blank to skip): ").strip()

    updates = {}
    if price_input:
        updates["price"] = float(price_input)
    if quantity_input:
        updates["quantity"] = int(quantity_input)

    if not updates:
        print("Nothing to update.")
        return

    resp = requests.patch(f"{API_BASE}/inventory/{item_id}", json=updates)
    if resp.status_code == 200:
        print("Item updated:", resp.json())
    else:
        print("Error:", resp.json())


def delete_item():
    item_id = input("Enter item ID to delete: ").strip()
    resp = requests.delete(f"{API_BASE}/inventory/{item_id}")
    if resp.status_code == 200:
        print(resp.json()["message"])
    else:
        print("Error:", resp.json())


def find_by_barcode():
    barcode = input("Enter barcode: ").strip()
    resp = requests.get(f"{API_BASE}/inventory/lookup/barcode/{barcode}")
    if resp.status_code == 200:
        print(resp.json())
    else:
        print("Error:", resp.json())


def find_by_name():
    name = input("Enter product name: ").strip()
    resp = requests.get(f"{API_BASE}/inventory/lookup/search", params={"name": name})
    if resp.status_code == 200:
        results = resp.json()
        if not results:
            print("No products found.")
        for product in results:
            print(f"- {product['product_name']} ({product['brands']}) "
                  f"barcode: {product['barcode']}")
    else:
        print("Error:", resp.json())


def add_from_barcode():
    barcode = input("Enter barcode: ").strip()
    price = _prompt_float("Price: ")
    quantity = _prompt_int("Quantity: ")
    resp = requests.post(
        f"{API_BASE}/inventory/lookup/barcode/{barcode}/add",
        json={"price": price, "quantity": quantity},
    )
    if resp.status_code == 201:
        print("Item added:", resp.json())
    else:
        print("Error:", resp.json())


def _prompt_float(label):
    while True:
        value = input(label).strip()
        if not value:
            return 0
        try:
            return float(value)
        except ValueError:
            print("Please enter a valid number.")


def _prompt_int(label):
    while True:
        value = input(label).strip()
        if not value:
            return 0
        try:
            return int(value)
        except ValueError:
            print("Please enter a valid whole number.")


ACTIONS = {
    "1": view_all,
    "2": view_item,
    "3": add_item,
    "4": update_item,
    "5": delete_item,
    "6": find_by_barcode,
    "7": find_by_name,
    "8": add_from_barcode,
}


def main():
    while True:
        print(MENU)
        choice = input("Select an option: ").strip()
        if choice == "0":
            print("Goodbye!")
            break
        action = ACTIONS.get(choice)
        if action is None:
            print("Invalid option, try again.")
            continue
        try:
            action()
        except requests.RequestException as exc:
            print(f"Could not reach the API server: {exc}")


if __name__ == "__main__":
    main()
