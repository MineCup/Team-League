from oauth2client.service_account import ServiceAccountCredentials
from apiclient import discovery
from httplib2 import Http
from TLBOT.config import table_key, table_id


def table():
    services = {"rating": None,
                "bot": None}

    credentials = ServiceAccountCredentials._from_parsed_json_keyfile({
        "type": "service_account",
        "project_id": "calm-mariner-304222",
        "private_key_id": table_id["id_1"],
        "private_key": table_key["key_1"].replace("\\n", "\n"),
        "client_email": "sxa-666@calm-mariner-304222.iam.gserviceaccount.com",
        "client_id": "104872701392314037045",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/sxa-666%40calm-mariner-304222.iam.gserviceaccount.com"
    },
        ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(Http())
    services["rating"] = discovery.build('sheets', 'v4', http=httpAuth)

    credentials = ServiceAccountCredentials._from_parsed_json_keyfile({
        "type": "service_account",
        "project_id": "calm-mariner-304222",
        "private_key_id": table_id["id_2"],
        "private_key": table_key["key_2"].replace("\\n", "\n"),
        "client_email": "sxa-1000@calm-mariner-304222.iam.gserviceaccount.com",
        "client_id": "113670012120547340229",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/sxa-1000%40calm-mariner-304222.iam.gserviceaccount.com"
    },
        ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(Http())
    services["bot"] = discovery.build('sheets', 'v4', http=httpAuth)
    return services
