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
            'product_info': '',
            'fabric_info': '',
            'product_measurements': '',
            'model_measurements': '',
            'size_info': ''
        }

        if not desc_text:
            return result

        clean_text = re.sub(r'<[^>]+>', ' ', desc_text)

        if 'Ürün Bilgisi:' in clean_text:
            result['product_info'] = re.search(r'Ürün Bilgisi:\s*([^:]+?)(?=\s*(?:Kumaş Bilgisi:|Ürün Ölçüleri:|Model Ölçüleri:|$))', clean_text)
            result['product_info'] = result['product_info'].group(1).strip() if result['product_info'] else ''

        if 'Kumaş Bilgisi:' in clean_text:
            result['fabric_info'] = re.search(r'Kumaş Bilgisi:\s*([^:]+?)(?=\s*(?:Ürün Ölçüleri:|Model Ölçüleri:|$))', clean_text)
            result['fabric_info'] = result['fabric_info'].group(1).strip() if result['fabric_info'] else ''

        if 'Ürün Ölçüleri:' in clean_text:
            result['product_measurements'] = re.search(r'Ürün Ölçüleri:?\s*([^:]+?)(?=\s*(?:Model Ölçüleri:|$))', clean_text)
            result['product_measurements'] = result['product_measurements'].group(1).strip() if result['product_measurements'] else ''

        if 'Model Ölçüleri:' in clean_text:
            result['model_measurements'] = re.search(r'Model Ölçüleri:\s*([^:]+?)(?=\s*(?:Modelin üzerindeki|$))', clean_text)
            result['model_measurements'] = result['model_measurements'].group(1).strip() if result['model_measurements'] else ''

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
                        'stock_code': product_id,
                        'name': name,
                        'color': [details.get('Color', '')],
                        'price': details.get('Price', '0'),
                        'discounted_price': details.get('DiscountedPrice', '0'),
                        'product_type': details.get('ProductType', ''),
                        'quantity': details.get('Quantity', '0'),
                        'series': details.get('Series', ''),
                        'season': details.get('Season', ''),
                        'images': images,
                        'fabric': parsed_desc['fabric_info'],
                        'model_measurements': parsed_desc['model_measurements'],
                        'product_measurements': parsed_desc['product_measurements'],
                        'product_info': parsed_desc['product_info']
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