import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timezone
from src.models import Product
from src.db_handler import MongoDBHandler


@pytest.fixture
def mock_products_collection():
    collection = MagicMock()
    collection.find_one.return_value = None
    collection.update_one.return_value = MagicMock(
        modified_count=0,
        upserted_id='123'
    )
    return collection


@pytest.fixture
def mock_db(mock_products_collection):
    db = MagicMock()
    db.products = mock_products_collection
    return db


@pytest.fixture
def mock_mongodb_client(mock_db):
    client = MagicMock()
    client.__getitem__.return_value = mock_db
    client.admin.command.return_value = True
    return client


@pytest.fixture
def db_handler(mock_mongodb_client):
    with patch('src.db_handler.MongoClient', return_value=mock_mongodb_client):
        handler = MongoDBHandler('fake_connection', 'test_db')
        yield handler
        handler.close()


def test_upsert_single_product(db_handler, mock_products_collection):
    test_product = Product(
        stock_code="TEST-001",
        name="Test Ürün",
        price=100.0,
        price_unit="Test",
        discounted_price=100.0,
        is_discounted=True,
        color=["Kırmızı"],
        quantity=10,
        product_type="Test",
        series="Test Series",
        season="2024",
        status="active",
        images=[],
        fabric="Test Fabric",
        model_measurements="Test Model",
        product_measurements="Test Product",
        createdAt=datetime.now(timezone.utc),
        updatedAt=datetime.now(timezone.utc)
    )

    db_handler.upsert_products([test_product])

    mock_products_collection.find_one.assert_called_once_with({'stock_code': 'TEST-001'})
    mock_products_collection.update_one.assert_called_once()


def test_update_existing_product(db_handler, mock_products_collection):
    mock_products_collection.find_one.return_value = {
        "stock_code": "TEST-002",
        "name": "Old Name",
        "createdAt": datetime.now(timezone.utc)
    }

    test_product = Product(
        stock_code="TEST-002",
        name="Updated Name",
        price=150.0,
        price_unit="Test",
        discounted_price=100.0,
        is_discounted=True,
        color=["Mavi"],
        quantity=10,
        product_type="Test",
        series="Test Series",
        season="2024",
        status="active",
        images=[],
        fabric="Test Fabric",
        model_measurements="Test Model",
        product_measurements="Test Product",
        createdAt=datetime.now(timezone.utc),
        updatedAt=datetime.now(timezone.utc)
    )

    db_handler.upsert_products([test_product])

    mock_products_collection.find_one.assert_called_once_with({'stock_code': 'TEST-002'})
    mock_products_collection.update_one.assert_called_once()


def test_database_error(db_handler, mock_products_collection):
    mock_products_collection.update_one.side_effect = Exception("DB Error")

    test_product = Product(
        stock_code="TEST-003",
        name="Test Ürün",
        price=100.0,
        price_unit="Test",
        discounted_price=100.0,
        is_discounted=True,
        color=["Kırmızı"],
        quantity=10,
        product_type="Test",
        series="Test Series",
        season="2024",
        status="active",
        images=[],
        fabric="Test Fabric",
        model_measurements="Test Model",
        product_measurements="Test Product",
        createdAt=datetime.now(timezone.utc),
        updatedAt=datetime.now(timezone.utc)
    )

    with pytest.raises(Exception) as exc_info:
        db_handler.upsert_products([test_product])

    assert str(exc_info.value) == "DB Error"


def test_connection_error():
    with patch('src.db_handler.MongoClient') as mock_client:
        mock_client.side_effect = Exception("Connection Error")

        with pytest.raises(Exception) as exc_info:
            MongoDBHandler('invalid_connection', 'test_db')

        assert str(exc_info.value) == "Connection Error"


def test_empty_product_list(db_handler, mock_products_collection):
    db_handler.upsert_products([])

    mock_products_collection.find_one.assert_not_called()
    mock_products_collection.update_one.assert_not_called()