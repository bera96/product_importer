import xml.etree.ElementTree as ET
from typing import List, Dict
from .models import Product
from io import BytesIO
from .data_formatter import DataFormatter
import re
from .logger import Logger

logger = Logger.get_logger()


class XMLParser:
    @staticmethod
    def _parse_description(desc_text: str) -> Dict[str, str]:
        result = {
            'fabric': '',
            'product_measurements': '',
            'model_measurements': '',
            'size_info': ''
        }

        if not desc_text:
            return result

        clean_text = re.sub(r'<[^>]+>', ' ', desc_text)
        clean_text = re.sub(r'&[a-zA-Z]+;', ' ', clean_text)

        patterns = {
            'fabric': r'Kumaş Bilgisi:?\s*(.*?)(?=Ürün Ölçüleri\d*:|Model Ölçüleri:|$)',
            'product_measurements': r'Ürün Ölçüleri\d*:?\s*(.*?)(?=Model Ölçüleri:|$)',
            'model_measurements': r'Model Ölçüleri:?\s*(.*?)(?=Modelin üzerindeki|Bedenler arası|$)',
        }

        for key, pattern in patterns.items():
            match = re.search(pattern, clean_text, re.DOTALL | re.IGNORECASE)
            if match:
                value = re.sub(r'\s+', ' ', match.group(1).strip())
                result[key] = value

        return result

    @staticmethod
    def parse_products(content: bytes) -> List[Product]:
        try:
            logger.info("XML content is being parsed")
            tree = ET.parse(BytesIO(content))
            root = tree.getroot()
            products = []

            product_elements = root.findall('./Product')
            total_products = len(product_elements)
            logger.info(f"Total {total_products} products found")

            for product_elem in product_elements:
                try:
                    product_id = product_elem.get('ProductId', '')
                    name = product_elem.get('Name', '')

                    images = [img.get('Path', '') for img in product_elem.findall('.//Image')]

                    details = {}
                    for detail in product_elem.findall('.//ProductDetail'):
                        detail_name = detail.get('Name', '')
                        detail_value = detail.get('Value', '')
                        details[detail_name] = detail_value

                    description = product_elem.find('.//Description')
                    desc_text = description.text if description is not None else ''
                    parsed_desc = XMLParser._parse_description(desc_text)

                    raw_data = {
                        'stock_code': product_id + '-' + details.get('Color', ''),
                        'name': name,
                        'color': [details.get('Color', '')],
                        'price': details.get('Price', '0'),
                        'discounted_price': details.get('DiscountedPrice', '0'),
                        'product_type': details.get('ProductType', ''),
                        'quantity': details.get('Quantity', '0'),
                        'series': details.get('Series', ''),
                        'season': details.get('Season', ''),
                        'images': images,
                        'fabric': parsed_desc['fabric'],
                        'model_measurements': parsed_desc['model_measurements'],
                        'product_measurements': parsed_desc['product_measurements'],
                    }

                    product_data = DataFormatter.format_product_data(raw_data)
                    products.append(Product(**product_data))
                    logger.debug(f"Product parsed: {product_id}")

                except Exception as e:
                    logger.error(f"Product parsing error ({product_id}): {str(e)}")
                    continue

            logger.info(f"Parsing process is completed. {len(products)} products processed successfully.")
            return products

        except Exception as e:
            logger.error(f"XML parsing error: {str(e)}")
            raise