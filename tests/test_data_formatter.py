from datetime import datetime, timezone
from src.data_formatter import DataFormatter


def test_format_price():
    assert DataFormatter.format_price("100,50") == 100.50
    assert DataFormatter.format_price("0,99") == 0.99

    assert DataFormatter.format_price("") == 0.0
    assert DataFormatter.format_price("0") == 0.0


def test_format_quantity():
    assert DataFormatter.format_quantity("100") == 100
    assert DataFormatter.format_quantity("0") == 0
    assert DataFormatter.format_quantity("42") == 42

    assert DataFormatter.format_quantity("") == 0
    assert DataFormatter.format_quantity("-1") == -1


def test_format_series():

    assert DataFormatter.format_series("") == ""
    assert DataFormatter.format_series("1") == "1"
    assert DataFormatter.format_series("S-M-L") == "S-M-L"


def test_format_product_data():
    raw_data = {
        'stock_code': ' TEST-001 ',
        'name': ' Test Product ',
        'color': [' Red ', ' Blue ', ''],
        'price': '100,50',
        'discounted_price': '90,00',
        'product_type': ' T-Shirt ',
        'quantity': '10',
        'series': '1S-2M-1L',
        'season': ' 2024 Summer ',
        'fabric': ' Cotton ',
        'model_measurements': ' Height: 180cm ',
        'product_measurements': ' Length: 70cm ',
        'images': ['image1.jpg', 'image2.jpg']
    }

    result = DataFormatter.format_product_data(raw_data)

    assert result['stock_code'] == 'TEST-001'
    assert result['name'] == 'Test Product'
    assert result['color'] == ['Red', 'Blue']
    assert result['price'] == 100.50
    assert result['price_unit'] == 'TRY'
    assert result['discounted_price'] == 90.00
    assert result['is_discounted'] is True
    assert result['product_type'] == 'T-Shirt'
    assert result['quantity'] == 10
    assert result['status'] == 'Active'
    assert result['series'] == 'S,M,M,L'
    assert result['season'] == '2024 Summer'
    assert result['fabric'] == 'Cotton'
    assert result['model_measurements'] == 'Height: 180cm'
    assert result['product_measurements'] == 'Length: 70cm'
    assert result['images'] == ['image1.jpg', 'image2.jpg']

    assert isinstance(result['createdAt'], datetime)
    assert isinstance(result['updatedAt'], datetime)
    assert result['createdAt'].tzinfo == timezone.utc
    assert result['updatedAt'].tzinfo == timezone.utc


def test_format_product_data_edge_cases():
    empty_data = {}
    result = DataFormatter.format_product_data(empty_data)

    assert result['stock_code'] == ''
    assert result['name'] == ''
    assert result['color'] == []
    assert result['price'] == 0.0
    assert result['discounted_price'] == 0.0
    assert result['is_discounted'] is False
    assert result['quantity'] == 0
    assert result['status'] == 'Inactive'

    no_discount_data = {
        'price': '100,00',
        'discounted_price': '0',
        'quantity': '5'
    }
    result = DataFormatter.format_product_data(no_discount_data)
    assert result['is_discounted'] is False
    assert result['status'] == 'Active'

    invalid_discount_data = {
        'price': '100,00',
        'discounted_price': '150,00'
    }
    result = DataFormatter.format_product_data(invalid_discount_data)
    assert result['is_discounted'] is False


def test_format_product_data_error():
    invalid_data = {
        'price': 'invalid',
        'quantity': 'invalid',
        'series': None
    }

    result = DataFormatter.format_product_data(invalid_data)
    assert result['price'] == 0.0
    assert result['quantity'] == 0
    assert result['series'] == ''
    assert result['status'] == 'Inactive'
