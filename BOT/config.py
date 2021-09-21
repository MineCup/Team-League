from os import environ

token = {"rucaptcha": str(environ.get("captcha")),
         "bot": str(environ.get('token'))}

user = {"login": str(environ.get('username')),
        "password": str(environ.get('password'))}

channels = {"map_pool": 858764823550623784,
            "team_league": 815244363633786910,
            "rating": 815938101901525002,
            "payload": 836007888010215454,
            "roles": 815231226927251487,
            "match_logs": 887056794457874443}

minecupRoles = {"tech": 853058142459789342,
                "org2": 803793187688808508,
                "org": 803793250103853067,
                "helper": 834496434953912381,
                "ss": 827620459008884756}
