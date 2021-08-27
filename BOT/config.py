from os import environ

token = {"rucaptcha": str(environ.get("captcha")),
         "bot": str(environ.get('token'))}

user = {"login": str(environ.get('username')),
        "password": str(environ.get('password'))}

channels = {"map_pool": 858026868354449468,
            "team_league": 858273631033360384,
            "rating": 856786719201427466,
            "payload": 858274393321898035,
            "roles": 858274158521352202,
            "match_logs": 858274100380172288}

minecupRoles = {"tech": 865158677791375381,
         "org2": 856785723934900234,
         "org": 856785670739984384,
         "helper2": 859522335392137217,
         "helper": 856785501356032000,
         "ss": 856953030514966528}
