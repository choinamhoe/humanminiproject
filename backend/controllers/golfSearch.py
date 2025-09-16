from fastapi.responses import JSONResponse
from fastapi import status
from pydantic import BaseModel
from services.golfSearch import post_services_golfSearchList
# POST로 받을 데이터 모델 정의
class GolfSearchRequest(BaseModel):
    search: str

async def post_controllers_golfSearchList(request: GolfSearchRequest):
    print("controllers post_controllers_golfSearchList start")
    try:
        res = post_services_golfSearchList(request.search)
        #print(f"controllers post_controllers_golfSearchList res : {res}")
        # res_dict = json.loads(res)
        return JSONResponse(    
            {"golfList":res},
            status_code=status.HTTP_200_OK
        )
        print(f"controllers post_controllers_golfSearchList end")
    except Exception as e:
        return JSONResponse(
            {"message":f"테스트 실패: {str(e)}"},
            status_code=status.HTTP_404_NOT_FOUND
        )
