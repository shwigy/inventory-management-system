from unittest.mock import MagicMock, patch

from src import cli


@patch("src.cli.requests.get")
def test_view_all_prints_items(mock_get, capsys):
    mock_response = MagicMock()
    mock_response.json.return_value = [
        {"id": 1, "product_name": "Almond Milk", "price": 3.99, "quantity": 10}
    ]
    mock_get.return_value = mock_response

    cli.view_all()
    captured = capsys.readouterr()
    assert "Almond Milk" in captured.out


@patch("src.cli.requests.get")
def test_view_all_empty(mock_get, capsys):
    mock_response = MagicMock()
    mock_response.json.return_value = []
    mock_get.return_value = mock_response

    cli.view_all()
    captured = capsys.readouterr()
    assert "No inventory items found." in captured.out


@patch("src.cli.requests.post")
@patch("builtins.input", side_effect=["Bread", "Wonder", "", "2.50", "5"])
def test_add_item(mock_input, mock_post, capsys):
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {"id": 1, "product_name": "Bread"}
    mock_post.return_value = mock_response

    cli.add_item()
    captured = capsys.readouterr()
    assert "Item added" in captured.out
    mock_post.assert_called_once()


@patch("src.cli.requests.delete")
@patch("builtins.input", return_value="1")
def test_delete_item(mock_input, mock_delete, capsys):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"message": "Item 1 deleted"}
    mock_delete.return_value = mock_response

    cli.delete_item()
    captured = capsys.readouterr()
    assert "Item 1 deleted" in captured.out
