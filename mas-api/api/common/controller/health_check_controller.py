from fastapi import APIRouter, status

router = APIRouter(tags=["Health Check"])


@router.get("/", status_code=status.HTTP_200_OK)
async def health_check():
    return {"message": "The Meeting Auto Summarization server is on."}
