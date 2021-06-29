from os import environ

token = {"rucaptcha": str(environ.get("captcha")),
         "bot": str(environ.get('token'))}

table_key = {"key_1": str(environ.get('key')).replace("\\n", "\n"),
             "key_2": str(environ.get('key_2')).replace("\\n", "\n")}

table_id = {"id_1": str(environ.get('k_id')),
            "id_2": str(environ.get('k_id_2'))}

sheet = {"team_league": "1OaMpmMMFR_NIzmqtEh12XJ6N4X9R723S4g709FKvj_8"}

user = {"login": str(environ.get('username')),
        "password": str(environ.get('password'))}

channels = {"map_pool": 858026868354449468,
            "team_league": 858273631033360384,
            "rating": 856786719201427466,
            "payload": 858274393321898035,
            "roles": 858274158521352202,
            "match_logs": 858274100380172288}

rolez = {"org2": 856785723934900234,
         "org": 856785670739984384,
         "helper2": 859522335392137217,
         "helper": 856785501356032000,
         "ss": 856953030514966528}

month = ["Янв.", "Фев.", "Марта", "Апр.", "Мая", "Июня", "Июля", "Авг.", "Сент.", "Окт.", "Нояб.", "Дек."]
month_num = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]

bw_ids = [858273631033360384, 856786815130533928]

heroku = "9c421f48-b043-48e8-add1-b7a5383f075f"
