from fastapi.responses import JSONResponse
from fastapi import status
from pydantic import BaseModel

from services.golfDetail import post_services_golfDetail

# POST로 받을 데이터 모델 정의
class GolfDetailRequest(BaseModel):
    id: int

async def post_controllers_golfDetail(request: GolfDetailRequest):
    print("controllers post_controllers_golfDetail start")

    try:
        res = post_services_golfDetail(request.id)
        #print(f"controllers post_controllers_golfDetail res : {res_dict}")
        print(f"controllers post_controllers_golfDetail res : {res}")
        #print(f"controllers post_services_golfDetail end ")
        return JSONResponse(    
            {"golfDetail":res},
            status_code=status.HTTP_200_OK
        )
    except Exception:
        return JSONResponse(
            {"message":"테스트 실패"},
            status_code=status.HTTP_404_NOT_FOUND
        )
