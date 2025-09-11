import os
from dotenv import load_dotenv

load_dotenv()  

config = {
    "FRONT_PORT": 3000,
    "BACKEND_PORT": 8000,
    "DB":{
        "USER_ID":"root",
        "PASSWORD":"15932!miniprojectdb",
        "HOST":"localhost",
        "PORT":"30000",
        "DATABASE_NAME":"miniproject"
    }
}
cors_config = {
    # "allow_origins":[
    #     f"http://localhost:{config['FRONT_PORT']}"
    #     ],
    "allow_origins":["*"],
    "allow_credentials":True,
    "allow_methods":["*"],
    "allow_headers":["*"],
}
