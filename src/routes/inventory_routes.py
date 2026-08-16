"""RESTful routes for CRUD operations on inventory items."""
from flask import Blueprint, jsonify, request

from src.models import inventory as inventory_model
from src.services import openfoodfacts

inventory_bp = Blueprint("inventory", __name__)


@inventory_bp.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify(inventory_model.get_all_items()), 200


@inventory_bp.route("/inventory/<int:item_id>", methods=["GET"])
def get_inventory_item(item_id):
    item = inventory_model.get_item(item_id)
    if item is None:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item), 200


@inventory_bp.route("/inventory", methods=["POST"])
def create_inventory_item():
    payload = request.get_json(silent=True)
    if not payload or "product_name" not in payload:
        return jsonify({"error": "product_name is required"}), 400

    item = {
        "product_name": payload.get("product_name"),
        "brands": payload.get("brands", ""),
        "barcode": payload.get("barcode", ""),
        "ingredients_text": payload.get("ingredients_text", ""),
        "price": payload.get("price", 0),
        "quantity": payload.get("quantity", 0),
    }
    created = inventory_model.add_item(item)
    return jsonify(created), 201


@inventory_bp.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_inventory_item(item_id):
    payload = request.get_json(silent=True)
    if not payload:
        return jsonify({"error": "No update data provided"}), 400

    updated = inventory_model.update_item(item_id, payload)
    if updated is None:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(updated), 200


@inventory_bp.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_inventory_item(item_id):
    deleted = inventory_model.delete_item(item_id)
    if not deleted:
        return jsonify({"error": "Item not found"}), 404
    return jsonify({"message": f"Item {item_id} deleted"}), 200


@inventory_bp.route("/inventory/lookup/barcode/<barcode>", methods=["GET"])
def lookup_by_barcode(barcode):
    try:
        product = openfoodfacts.get_product_by_barcode(barcode)
    except openfoodfacts.OpenFoodFactsError as exc:
        return jsonify({"error": str(exc)}), 502

    if product is None:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product), 200


@inventory_bp.route("/inventory/lookup/search", methods=["GET"])
def lookup_by_name():
    name = request.args.get("name")
    if not name:
        return jsonify({"error": "name query parameter is required"}), 400

    try:
        products = openfoodfacts.search_products_by_name(name)
    except openfoodfacts.OpenFoodFactsError as exc:
        return jsonify({"error": str(exc)}), 502

    return jsonify(products), 200


@inventory_bp.route("/inventory/lookup/barcode/<barcode>/add", methods=["POST"])
def add_item_from_barcode(barcode):
    """Fetch a product from OpenFoodFacts and add it directly to inventory."""
    try:
        product = openfoodfacts.get_product_by_barcode(barcode)
    except openfoodfacts.OpenFoodFactsError as exc:
        return jsonify({"error": str(exc)}), 502

    if product is None:
        return jsonify({"error": "Product not found"}), 404

    payload = request.get_json(silent=True) or {}
    item = {
        "product_name": product["product_name"],
        "brands": product["brands"],
        "barcode": product["barcode"],
        "ingredients_text": product["ingredients_text"],
        "price": payload.get("price", 0),
        "quantity": payload.get("quantity", 0),
    }
    created = inventory_model.add_item(item)
    return jsonify(created), 201
