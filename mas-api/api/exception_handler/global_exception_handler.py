from fastapi import Request
from fastapi.responses import JSONResponse


async def global_exception_handler(request: Request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "message": f"There is a problem with the mas-api server for a moment. Please try again in a few minutes!"
        },
    )
