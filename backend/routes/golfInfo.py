from fastapi import APIRouter

from controllers import golfInfo,golfDetail

print("routes start")
router = APIRouter()

router.add_api_route("/",golfInfo.post_controllers_golfList, methods=["POST"])
router.add_api_route("/detail",golfDetail.post_controllers_golfDetail, methods=["POST"])
print("routes end")