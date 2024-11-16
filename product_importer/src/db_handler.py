from pymongo import MongoClient
from typing import List
import logging
from .models import Product

logger = logging.getLogger(__name__)


class MongoDBHandler:
    def __init__(self, connection_string: str, db_name: str):
        try:
            logger.info("MongoDB connection is starting...")
            self.client = MongoClient(connection_string)
            self.db = self.client[db_name]
            self.products = self.db.products

            self.client.admin.command('ping')
            logger.info("MongoDB connection is successful!")

        except Exception as e:
            logger.error(f"MongoDB connection error: {str(e)}")
            raise

    def upsert_products(self, products: List[Product]):
        try:
            logger.info(f"{len(products)} products are being added...")
            for product in products:
                self.products.update_one(
                    {'stock_code': product.stock_code},
                    {'$set': product.model_dump()},
                    upsert=True
                )
                logger.debug(f"Product updated/added: {product.stock_code}")

            logger.info("All products have been updated/added successfully!")

        except Exception as e:
            logger.error(f"Product adding error: {str(e)}")
            raise

    def close(self):
        try:
            self.client.close()
            logger.info("MongoDB connection is closed")
        except Exception as e:
            logger.error(f"Connection closing error: {str(e)}")