from unittest.mock import MagicMock, patch

import pytest

from src.services import openfoodfacts


@patch("src.services.openfoodfacts.requests.get")
def test_get_product_by_barcode_found(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "status": 1,
        "product": {
            "product_name": "Organic Almond Milk",
            "brands": "Silk",
            "ingredients_text": "Filtered water, almonds, cane sugar",
        },
    }
    mock_response.raise_for_status = MagicMock()
    mock_get.return_value = mock_response

    product = openfoodfacts.get_product_by_barcode("1234567890")
    assert product["product_name"] == "Organic Almond Milk"
    assert product["brands"] == "Silk"
    assert product["barcode"] == "1234567890"


@patch("src.services.openfoodfacts.requests.get")
def test_get_product_by_barcode_not_found(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {"status": 0}
    mock_response.raise_for_status = MagicMock()
    mock_get.return_value = mock_response

    product = openfoodfacts.get_product_by_barcode("0000000000")
    assert product is None


@patch("src.services.openfoodfacts.requests.get")
def test_get_product_by_barcode_request_error(mock_get):
    import requests

    mock_get.side_effect = requests.RequestException("network error")

    with pytest.raises(openfoodfacts.OpenFoodFactsError):
        openfoodfacts.get_product_by_barcode("1234567890")


@patch("src.services.openfoodfacts.requests.get")
def test_search_products_by_name(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "products": [
            {"product_name": "Almond Milk", "brands": "Silk", "code": "111"},
            {"product_name": "Oat Milk", "brands": "Oatly", "code": "222"},
        ]
    }
    mock_response.raise_for_status = MagicMock()
    mock_get.return_value = mock_response

    results = openfoodfacts.search_products_by_name("milk")
    assert len(results) == 2
    assert results[0]["product_name"] == "Almond Milk"


@patch("src.routes.inventory_routes.openfoodfacts.get_product_by_barcode")
def test_lookup_by_barcode_route_found(mock_lookup, client):
    mock_lookup.return_value = {
        "barcode": "123",
        "product_name": "Almond Milk",
        "brands": "Silk",
        "ingredients_text": "",
        "categories": "",
        "image_url": "",
    }
    resp = client.get("/inventory/lookup/barcode/123")
    assert resp.status_code == 200
    assert resp.get_json()["product_name"] == "Almond Milk"


@patch("src.routes.inventory_routes.openfoodfacts.get_product_by_barcode")
def test_lookup_by_barcode_route_not_found(mock_lookup, client):
    mock_lookup.return_value = None
    resp = client.get("/inventory/lookup/barcode/123")
    assert resp.status_code == 404


@patch("src.routes.inventory_routes.openfoodfacts.get_product_by_barcode")
def test_add_item_from_barcode_route(mock_lookup, client):
    mock_lookup.return_value = {
        "barcode": "123",
        "product_name": "Almond Milk",
        "brands": "Silk",
        "ingredients_text": "water, almonds",
        "categories": "",
        "image_url": "",
    }
    resp = client.post("/inventory/lookup/barcode/123/add", json={"price": 4.5, "quantity": 3})
    assert resp.status_code == 201
    body = resp.get_json()
    assert body["product_name"] == "Almond Milk"
    assert body["price"] == 4.5
