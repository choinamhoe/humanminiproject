from models.golfInfo import post_model_golfList

def post_services_golfList():
   print("services post_services_golfList start")
   res = post_model_golfList()
   print(f"services post_services_golfList end")
   return res