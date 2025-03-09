import json
from fastapi import APIRouter, Depends, File, Request, UploadFile
import redis
from scalar_fastapi import get_scalar_api_reference
from app.routers.track import track_router
from app.routers.video import video_router
from app.services.files import get_url
from aiogram import types
from bot.bot import bot
from app.core.config import settings
router = APIRouter()

@router.get("/scalar", include_in_schema=False)
def get_api_reference():
    from app.app import app
    return get_scalar_api_reference(
        title=app.title,
        openapi_url=app.openapi_url
    )
@router.post("/test-bucket")
async def testing_bucket(file: UploadFile = File(...)):
    url = await get_url([file])
    return url

@router.post("/create-invoice")
async def create_invoice(web_app_data: str, redis_client: redis.Redis = Depends(settings.get_redis)):
    web_app_data = json.loads(web_app_data)
    payload = json.loads(web_app_data["payload"])
    if web_app_data["payload"]:
        redis_client.set(payload["id"], web_app_data["payload"])
    price = [types.LabeledPrice(label="Pay", amount=int(web_app_data["prices"]) * 100)]
    link = await bot.create_invoice_link(
        title=web_app_data["title"],
        description=web_app_data["description"],
        payload=payload["id"], #web_app_data["payload"],
        currency=web_app_data["currency"],
        prices=price,
        provider_token="381764678:TEST:114664",
        need_email=True,
        need_phone_number=True
    )
    return link


router.include_router(track_router)
router.include_router(video_router)