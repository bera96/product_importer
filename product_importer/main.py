from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.db_handler import MongoDBHandler
from typing import AsyncGenerator
from src.api.v1.routes import router as v1_router, executor
from src.logger import Logger

logger = Logger.get_logger()


async def lifespan(app: FastAPI) -> AsyncGenerator:
    try:
        logger.info("Application is starting...")
        db_handler = MongoDBHandler(
            connection_string="connection_string",  # add connection string here later
            db_name="product_importer"
        )
        app.state.db_handler = db_handler
        logger.info("MongoDB connection is ready!")

        yield

    except Exception as e:
        logger.error(f"Startup error: {str(e)}")
        raise
    finally:
        logger.info("Application is shutting down...")
        executor.shutdown(wait=True)
        if hasattr(app.state, 'db_handler'):
            app.state.db_handler.close()

app = FastAPI(
    title="Product Importer API",
    description="XML Product Import API with MongoDB Integration",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)