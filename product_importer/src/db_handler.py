from pymongo import MongoClient
from typing import List
from datetime import datetime, timezone
from .models import Product
from .logger import Logger

logger = Logger.get_logger()

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
            for product in products:
                product_data = product.model_dump()

                now = datetime.now(timezone.utc)

                existing_product = self.products.find_one({'stock_code': product.stock_code})

                if existing_product:
                    product_data['updatedAt'] = now
                    product_data.pop('createdAt', None)
                    logger.info(f"Product updating: {product.stock_code}")
                else:
                    product_data['createdAt'] = now
                    product_data['updatedAt'] = now
                    logger.info(f"New product is being adding: {product.stock_code}")

                result = self.products.update_one(
                    {'stock_code': product.stock_code},
                    {'$set': product_data},
                    upsert=True
                )

                if result.modified_count:
                    logger.info(f"Product updated: {product.stock_code}")
                elif result.upserted_id:
                    logger.info(f"New product is being added: {product.stock_code}")

            logger.info("All products are successfully added/updated!")

        except Exception as e:
            logger.error(f"Product adding/updating error: {str(e)}")
            raise

    def close(self):
        try:
            self.client.close()
            logger.info("MongoDB connection is closed")
        except Exception as e:
            logger.error(f"Connection closing error: {str(e)}")