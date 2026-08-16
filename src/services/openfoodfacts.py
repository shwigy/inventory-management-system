"""Client for the OpenFoodFacts external API."""
import requests

BASE_URL = "https://world.openfoodfacts.org"
TIMEOUT = 10


class OpenFoodFactsError(Exception):
    pass


def get_product_by_barcode(barcode):
    """Fetch a single product by barcode. Returns a dict or None if not found."""
    url = f"{BASE_URL}/api/v2/product/{barcode}.json"
    try:
        response = requests.get(url, timeout=TIMEOUT)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise OpenFoodFactsError(str(exc)) from exc

    data = response.json()
    if data.get("status") != 1:
        return None
    return _extract_product(data["product"], barcode=barcode)


def search_products_by_name(name, page_size=5):
    """Search products by name. Returns a list of product dicts."""
    url = f"{BASE_URL}/cgi/search.pl"
    params = {
        "search_terms": name,
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page_size": page_size,
    }
    try:
        response = requests.get(url, params=params, timeout=TIMEOUT)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise OpenFoodFactsError(str(exc)) from exc

    data = response.json()
    products = data.get("products", [])
    return [_extract_product(p) for p in products]


def _extract_product(product, barcode=None):
    return {
        "barcode": barcode or product.get("code"),
        "product_name": product.get("product_name") or "Unknown",
        "brands": product.get("brands") or "Unknown",
        "ingredients_text": product.get("ingredients_text") or "",
        "categories": product.get("categories") or "",
        "image_url": product.get("image_url") or "",
    }
