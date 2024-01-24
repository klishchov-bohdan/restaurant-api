import asyncio

from fastapi import FastAPI
from app.services import menu_router, submenu_router, dish_router


app = FastAPI()

# origins = ["*"]
#
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

app.include_router(menu_router, prefix='/api/v1')
app.include_router(submenu_router, prefix='/api/v1')
app.include_router(dish_router, prefix='/api/v1')

