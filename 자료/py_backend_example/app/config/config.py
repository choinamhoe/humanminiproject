import os
from dotenv import load_dotenv

load_dotenv()  

config = {
    "FRONT_PORT": 3000,
    "BACKEND_PORT": 5001,
    "DB":{
        "USER_ID":"",
        "PASSWORD":"",
        "HOST":"localhost:3307"
    }
}
cors_config = {
    "allow_origins":[
        f"http://localhost:{config['FRONT_PORT']}"
        ],
    #  "allow_origins":["*"],
    "allow_credentials":True,
    "allow_methods":["*"],
    "allow_headers":["*"],
}
