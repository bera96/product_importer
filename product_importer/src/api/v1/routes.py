from fastapi import APIRouter, UploadFile, File, Request, HTTPException
from typing import Dict, Union
from ...xml_parser import XMLParser
import asyncio
from concurrent.futures import ThreadPoolExecutor
from ...logger import Logger

router = APIRouter()
executor = ThreadPoolExecutor(max_workers=4)
logger = Logger.get_logger()

async def parse_products_async(content: bytes) -> list:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, XMLParser.parse_products, content)

async def get_db(request):
    return request.app.state.db_handler

@router.post("/import-products")
async def import_products(
    file: Union[UploadFile, None] = File(None),
    request: Request = Request
) -> Dict:
    try:
        if file:
            content = await file.read()
            logger.info(f"File received via form-data: {file.filename}")

        else:
            content = await request.body()
            logger.info(f"Content received via request body")

        if not content:
            raise HTTPException(status_code=400, detail="No content provided")
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