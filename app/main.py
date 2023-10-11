import time, secrets
from typing import Annotated
from fastapi import FastAPI, Depends, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.configs.settings import settings
from app.core.database.indexes import DatabaseIndexManager
from app.core.enum.event_types import EventTypes
from app.core.services.response_service import responseService
from app.dependencies.database import get_main_db
from app.endpoints.tasks import router as tasks_router
from app.endpoints.users import router as users_router

router = APIRouter(prefix='/api')


@router.get("/")
async def root():
    return {"message": "Let's be happy yo."}


@router.get("/hello/{name}")
async def health_test(name: str, message: str = '', db: AsyncIOMotorDatabase = Depends(get_main_db)):
    message = 'you said ' + message if message else ''
    resp = {
        'message': f"Hello {name}. It seems working fine ^_^. {message}"
    }
    return JSONResponse(resp, 200)


router.include_router(users_router)
router.include_router(tasks_router)

app = FastAPI(
    title=settings.PROJECT_NAME,
    summary="this is the back-end side of the open source project called let's be happy.",
    description="Further information will be published soon",
    version="1.0.0",
    docs_url=None,
    redoc_url=None,
    openapi_url='/' + settings.OPENAPI_URL
)

app.include_router(router)
app.add_event_handler(EventTypes.STARTUP, DatabaseIndexManager.crete_indexes)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware('http')
async def process_time_response(request, call_next):
    start = time.time()
    response = await call_next(request)
    end = time.time()
    response.headers['X-processd-ms'] = str(1000 * (end - start))  # in milli seconds
    return response


@app.get("/docs", include_in_schema=False)
async def get_swagger_api_docs(credentials: Annotated[HTTPBasicCredentials, Depends(HTTPBasic())]):
    if secrets.compare_digest(credentials.username, settings.DOC_USERNAME) and secrets.compare_digest(credentials.password, settings.DOC_PASSWORD):
        return get_swagger_ui_html(
            openapi_url=app.openapi_url,
            title=app.title + " - Swagger UI",
        )
    
    return responseService.error_403('wrong username or password given')


@app.get("/redoc", include_in_schema=False)
async def get_redoc_api_docs(credentials: Annotated[HTTPBasicCredentials, Depends(HTTPBasic())]):
    if secrets.compare_digest(credentials.username, settings.DOC_USERNAME) and secrets.compare_digest(credentials.password, settings.DOC_PASSWORD):
        return get_redoc_html(
            openapi_url=app.openapi_url,
            title=app.title + " - ReDoc",
        )

    return responseService.error_403('wrong username or password given')    
