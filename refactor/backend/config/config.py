from dotenv import dotenv_values
config = dotenv_values()
config["HOST"] = "localhost"

cors_config = {
    # "allow_origins":[
    #     f"http://localhost:{config['FRONT_PORT']}"
    #     ],
    "allow_origins":["*"],
    "allow_credentials":True,
    "allow_methods":["*"],
    "allow_headers":["*"],
}
