from fastapi import FastAPI

from mas.utils.controller_utils import get_controllers

app = FastAPI()
modules = get_controllers("./")

for module in modules:
    router = module.router
    app.include_router(router)
