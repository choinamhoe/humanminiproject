from fastapi.responses import JSONResponse
from fastapi import status
import json

from services.golfInfo import post_services_golfList

async def post_controllers_golfList():
    print("controllers post_controllers_golfList start")
    try:
        res = post_services_golfList()
        print(f"controllers post_controllers_golfList res : {res}")
        res_dict = json.loads(res)
        return JSONResponse(    
            {"golfList":res_dict},
            status_code=status.HTTP_200_OK
        )
        print(f"controllers post_controllers_golfList end")
        
    except Exception:
        return JSONResponse(
            {"message":"테스트 실패"},
            status_code=status.HTTP_404_NOT_FOUND
        )
