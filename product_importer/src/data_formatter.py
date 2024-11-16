from typing import Dict, Any
from datetime import datetime, timezone
from .logger import Logger
import re

logger = Logger.get_logger()


class DataFormatter:
    @staticmethod
    def format_price(price: str) -> float:
        try:
            cleaned_price = price.replace(',', '.').strip()
            return float(cleaned_price)
        except Exception as e:
            logger.warning(f"Price formatting error: {str(e)}")
            return 0.0

    @staticmethod
    def format_quantity(quantity: str) -> int:
        try:
            return int(quantity)
        except Exception as e:
            logger.warning(f"Quantity formatting error: {str(e)}")
            return 0

    @staticmethod
    def format_series(series: str) -> str:
        try:
            if not series:
                return ''

            result = []
            parts = series.split('-')

            for part in parts:
                if not part:
                    continue
                count = int(re.match(r'(\d+)', part).group(1))
                size = re.search(r'[A-Za-z]+', part).group()
                result.extend([size] * count)

            return ','.join(result)
        except Exception as e:
            logger.warning(f"Series formatting error: {str(e)}")
            return series

    @staticmethod
    def format_product_data(raw_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            price = DataFormatter.format_price(raw_data.get('price', '0'))
            discounted_price = DataFormatter.format_price(raw_data.get('discounted_price', '0'))

            is_discounted = discounted_price > 0 and discounted_price < price

            return {
                'stock_code': raw_data.get('stock_code', '').strip(),
                'name': raw_data.get('name', '').strip(),
                'color': [color.strip() for color in raw_data.get('color', []) if color],
                'price': price,
                'price_unit': 'TRY',
                'discounted_price': discounted_price,
                'is_discounted': is_discounted,
                'product_type': raw_data.get('product_type', '').strip(),
                'quantity': DataFormatter.format_quantity(raw_data.get('quantity', '0')),
                'status': 'Active' if DataFormatter.format_quantity(raw_data.get('quantity', '0')) > 0 else 'Inactive',
                'sample_size': DataFormatter.format_series(raw_data.get('series', '')),
                'series': raw_data.get('season', '').strip(),
                'fabric': raw_data.get('fabric', '').strip(),
                'model_measurements': raw_data.get('model_measurements', '').strip(),
                'product_measurements': raw_data.get('product_measurements', '').strip(),
                'images': raw_data.get('images', []),
                'createdAt': datetime.now(timezone.utc),
                'updatedAt': datetime.now(timezone.utc)
            }
        except Exception as e:
            logger.error(f"Product data formatting error: {str(e)}")
            raise
