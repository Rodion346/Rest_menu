from fastapi import FastAPI
from routes.menu_routers import router as menu_router
from routes.submenu_routers import router as submenu_router
from routes.dish_routers import router as dish_router

app = FastAPI()


app.include_router(menu_router)
app.include_router(submenu_router)
app.include_router(dish_router)