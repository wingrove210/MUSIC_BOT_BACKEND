from fastapi import APIRouter, File, UploadFile
from scalar_fastapi import get_scalar_api_reference
from app.routers.track import track_router
from app.routers.video import video_router
from app.services.files import get_url
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
router.include_router(track_router)
router.include_router(video_router)