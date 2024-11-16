from fastapi import APIRouter, UploadFile, File, Depends, Request
from typing import Dict
from ...xml_parser import XMLParser
from ...db_handler import MongoDBHandler
import asyncio
from concurrent.futures import ThreadPoolExecutor

router = APIRouter()
executor = ThreadPoolExecutor(max_workers=4)


async def parse_products_async(content: bytes) -> list:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, XMLParser.parse_products, content)


async def get_db(request):
    return request.app.state.db_handler


@router.post("/import-products")
async def import_products(
    file: UploadFile = File(...),
    request: Request = Request
) -> Dict:
    try:
        content = await file.read()
        products = await parse_products_async(content)
        db_handler = request.app.state.db_handler
        db_handler.upsert_products(products)

        return {
            "success": True,
            "message": f"{len(products)} products successfully imported",
            "imported_count": len(products),
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error occurred: {str(e)}",
            "imported_count": 0,
        }