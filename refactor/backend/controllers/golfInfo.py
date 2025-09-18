from fastapi.responses import JSONResponse
from fastapi import status

from services.golfInfo import post_services_golfList

async def post_controllers_golfList():
    print("controllers post_controllers_golfList start")
    try:
        res = post_services_golfList()
        return JSONResponse(    
            {"golfList":res},
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        return JSONResponse(
            {"message":f"테스트 실패: {str(e)}"},
            status_code=status.HTTP_404_NOT_FOUND
        )
