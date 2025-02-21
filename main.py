import asyncio
import uvicorn

async def fastapi():
    uvicorn.run("app.app:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    asyncio.run(fastapi())