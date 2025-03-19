import json
from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile, status
import redis
from scalar_fastapi import get_scalar_api_reference
from app.routers.track import track_router
from app.routers.video import video_router
from app.services.files import get_url
from aiogram import types
from bot.bot import bot
from app.core.config import settings
from app.schemas.schemas import MessageType
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

@router.post("/save-data")
async def save_data_to_redis(data: MessageType, redis_client: redis.Redis = Depends(settings.get_redis)):
    try:
        payload_id = data.id
        redis_client.set(payload_id, data.model_dump_json())
        return {"ok": True, "payload": payload_id}
    except Exception as e:
        payload_id = data.id
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"ok": False, "payload": payload_id, "error": str(e)})

@router.post("/create-invoice")
async def create_invoice(web_app_data: str, redis_client: redis.Redis = Depends(settings.get_redis)):
    # print(web_app_data)
    web_app_data = json.loads(web_app_data)
    print(web_app_data["payload"])
    price = [types.LabeledPrice(label="Pay", amount=int(web_app_data["prices"]) * 100)]
    link = await bot.create_invoice_link(
        title=web_app_data["title"],
        description=web_app_data["description"],
        payload=web_app_data["payload"], #web_app_data["payload"],
        currency=web_app_data["currency"],
        prices=price,
        provider_token=settings.YOOKASSA_TG_TEST_API if settings.ENVIRONMENT == "development" else settings.YOOKASSA_TG_API,
        provider_data=json.dumps(web_app_data["provider_data"]),
        need_email=True,
        send_email_to_provider=True,
        photo_url="https://storage.yandexcloud.net/patriot-music/Frame%2095.png"
    )
    
    return link


router.include_router(track_router)
router.include_router(video_router)