import fastapi
from api.routers import auth
from api.routers.holidays import router


app = fastapi.FastAPI()
app.include_router(router)
app.include_router(auth.router)
