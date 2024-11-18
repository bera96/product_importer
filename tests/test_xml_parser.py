import pytest
from src.xml_parser import XMLParser
from src.models import Product


@pytest.fixture
def sample_xml_content():
    return """<?xml version="1.0"?>
    <Products>
        <Product ProductId="27356-01" Name="TEST URUN">
            <Images>
                <Image Path="test1.jpg"></Image>
                <Image Path="test2.jpg"></Image>
            </Images>
            <ProductDetails>
                <ProductDetail Name="Price" Value="5,24"/>
                <ProductDetail Name="DiscountedPrice" Value="2,24"/>
                <ProductDetail Name="ProductType" Value="Test"/>
                <ProductDetail Name="Quantity" Value="9"/>
                <ProductDetail Name="Color" Value="Kirmizi"/>
                <ProductDetail Name="Series" Value="1S-1M-2L-1XL"/>
                <ProductDetail Name="Season" Value="2024 Yaz"/>
            </ProductDetails>
            <Description>
                <![CDATA[<ul><li><strong>Ürün Bilgisi:</strong>Test açıklama</li>
                <li><strong>Kumaş Bilgisi:</strong>%100 Pamuk</li>
                <li><strong>Ürün Ölçüleri:</strong>Boy: 62 cm</li>
                <li><strong>Model Ölçüleri:</strong>Boy: 1.74</li></ul>]]>
            </Description>
        </Product>
    </Products>""".encode('utf-8')


def test_parse_description():
    desc = """<![CDATA[<ul>
        <li><strong>Ürün Bilgisi:</strong>Test ürün</li>
        <li><strong>Kumaş Bilgisi:</strong>%100 Pamuk</li>
        <li><strong>Ürün Ölçüleri:</strong>Boy: 100cm</li>
        <li><strong>Model Ölçüleri:</strong>Boy: 1.70</li>
    </ul>]]>"""

    result = XMLParser._parse_description(desc)

    assert '%100 Pamuk' in result['fabric']
    assert 'Boy: 100cm' in result['product_measurements']
    assert 'Boy: 1.70' in result['model_measurements']


def test_parse_products(sample_xml_content):
    products = XMLParser.parse_products(sample_xml_content)

    assert len(products) == 1
    product = products[0]

    assert isinstance(product, Product)
    assert product.stock_code == "27356-01-Kirmizi"
    assert product.name == "TEST URUN"
    assert product.price == 5.24
    assert product.discounted_price == 2.24
    assert product.quantity == 9