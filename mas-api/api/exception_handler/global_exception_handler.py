from fastapi import Request
from fastapi.responses import JSONResponse


async def global_exception_handler(request: Request, exc):
    return JSONResponse(
        status_code=500,
        content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
    )
