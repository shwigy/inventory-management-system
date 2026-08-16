def test_get_inventory_empty(client):
    resp = client.get("/inventory")
    assert resp.status_code == 200
    assert resp.get_json() == []


def test_create_and_get_item(client):
    resp = client.post("/inventory", json={
        "product_name": "Almond Milk",
        "brands": "Silk",
        "price": 3.99,
        "quantity": 10,
    })
    assert resp.status_code == 201
    created = resp.get_json()
    assert created["id"] == 1
    assert created["product_name"] == "Almond Milk"

    resp = client.get(f"/inventory/{created['id']}")
    assert resp.status_code == 200
    assert resp.get_json()["product_name"] == "Almond Milk"


def test_create_item_missing_name(client):
    resp = client.post("/inventory", json={"brands": "Silk"})
    assert resp.status_code == 400


def test_get_item_not_found(client):
    resp = client.get("/inventory/999")
    assert resp.status_code == 404


def test_update_item(client):
    created = client.post("/inventory", json={"product_name": "Cereal"}).get_json()
    resp = client.patch(f"/inventory/{created['id']}", json={"price": 5.49, "quantity": 20})
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["price"] == 5.49
    assert body["quantity"] == 20


def test_update_item_not_found(client):
    resp = client.patch("/inventory/999", json={"price": 1})
    assert resp.status_code == 404


def test_delete_item(client):
    created = client.post("/inventory", json={"product_name": "Bread"}).get_json()
    resp = client.delete(f"/inventory/{created['id']}")
    assert resp.status_code == 200

    resp = client.get(f"/inventory/{created['id']}")
    assert resp.status_code == 404


def test_delete_item_not_found(client):
    resp = client.delete("/inventory/999")
    assert resp.status_code == 404
