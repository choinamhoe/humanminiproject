from fastapi.responses import JSONResponse
from fastapi import status

from services.test import get_hello_message
async def say_hello():
    try:
        res = get_hello_message()
        return JSONResponse(    
            {"message":res},
            status_code=status.HTTP_200_OK
        )
    except Exception:
        return JSONResponse(
            {"message":"테스트 실패"},
            status_code=status.HTTP_404_NOT_FOUND
        )
