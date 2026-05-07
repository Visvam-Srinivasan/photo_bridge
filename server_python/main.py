import uvicorn
from fastapi import FastAPI
from api.routes import router
from discovery import DiscoveryService
import contextlib

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    discovery = DiscoveryService(port=8080)
    discovery.register()
    yield
    discovery.unregister()

app = FastAPI(
    lifespan=lifespan,
    title="FileBridge server",
    description="Local network file transfer backend"
)

app.include.router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)