from fastapi import APIRouter

from controllers import golfInfo

print("routes start")
router = APIRouter()
router.add_api_route("/",golfInfo.post_controllers_golfList, methods=["POST"])
print("routes end")