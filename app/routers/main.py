import json
import logging
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
        redis_client.info("replication")
        redis_client.set(payload_id, data.model_dump_json())  # Для Pydantic V2
        return {"ok": True, "payload": payload_id}
    except Exception as e:
        logging.error(f"Ошибка сохранения данных в Redis: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail={"ok": False, "payload": payload_id, "error": str(e)}
        )

@router.post("/create-invoice")
async def create_invoice(web_app_data: str, redis_client: redis.Redis = Depends(settings.get_redis)):
    try:
        web_app_data = json.loads(web_app_data)
    except json.JSONDecodeError as e:
        logging.error(f"Ошибка парсинга JSON: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Неверный формат JSON"
        )

    try:
        payload = web_app_data["payload"]
        logging.info(f"Создание инвойса для payload: {payload}")

        price = [types.LabeledPrice(label="Оплата", amount=int(web_app_data["prices"]) * 100)]
        link = await bot.create_invoice_link(
            title=web_app_data["title"],
            description=web_app_data["description"],
            payload=payload,
            currency=web_app_data["currency"],
            prices=price,
            provider_token=settings.YOOKASSA_TG_TEST_API if settings.ENVIRONMENT == "development" else settings.YOOKASSA_TG_API,
            provider_data=json.dumps(web_app_data.get("provider_data", {})),
            need_email=True,
            send_email_to_provider=True,
            photo_url=settings.INVOICE_PHOTO_URL
        )

        return link
    except Exception as e:
        logging.error(f"Ошибка при создании инвойса: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Ошибка при создании платежной ссылки"
        )



router.include_router(track_router)
router.include_router(video_router)