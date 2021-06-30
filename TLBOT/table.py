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
        "private_key_id": "d646789cdd016b0c4c4176c07345dccf1f1a6866",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDSzhhcXqeTR2zT\nh1tjz4U9dN4DliwyUGwaz83DtSKFJQZz910fs+sEBjUnv9zTDSlHucA5nc2xs7qs\nd0mMtyAo4vOXuXdLMPon12iFQDQB/8va2Sd5+F3E8yuyycXGySIs5ugkvQ0BKzQR\nGOjG/bEcsgiGV8dQMg9SFLPFs+LEZ/kQWeTtAMrHgaygUzJZqL/ebhQ3QGmJ3N1z\n691f28gqva3QM3pDYhrq4NfYxBK9L28XKa1OlfqZyKSwUvyfj29C6UDPZcM9Toed\njy7ICujd9CCzEGR7NKBBlP4GaVl46Y4DZhlmavI3xBnLpUzu566vDx2qAs7GUUhi\nuSTe1IpdAgMBAAECggEABwYyhhtqUoxB+k9rkmkXC7vx7OUrXlbTL1aGyPNnbc/U\nxfbzXavRVC4/xa4NNeQdoMP1/YV+VeJDAV2tL/jnI62iR8c4jCMa5sp082G3Ce0D\n1iw/tj76IuamaVvzUOMhViUwjY7WGNifcMVndj/8T5Q4F//jRo8Qdx/0+Iy8rOYp\nhjuw1jlm3KapggrsH3u/kF6SZICYJUbqct7THtl14/5jz0PHnDHjZXciVbwQhHzh\ntUCb8eT8346OY7Pod58in+10ot5cQ/Qmt7LOVFOtX16EkVb3TZHyBGj5PAVpctAP\njlJvc6/fi+UXL9dlqVtQm7NlxTkKAv0IZApDtCwGGQKBgQDxyMfnMWIroX+Y8FpN\nnQpo7Z+s4ER0/kScKaT9Kdwyoiu1lyqIgxR0d2EjyJlVn3KfgKHzYGwFb3c1gjuz\nxiz4BnMuvp3p3rrwmoYh//2ymuqN4atvgDh1JAzGCnmz9YCvcHefxo77gOX+3Mys\nyjlGwEBj7K6HYNiK23lIxowMiQKBgQDfMwem7zOyv7j3NLarMCnO0seS2kDl750X\n9mV5StOQyoIbqqYxcGldQivC2XY7+1AsvY9LNOP4NUIN4OPFhPAjWeBcaOEJqRXt\n1oPBtazTbpJbxB05nTOblbGGcMv7ppPR9Mo4FCvjDATPiHc1HL3iaBSvhsf8e8T0\nJhPIO13iNQKBgQDp/hdArrFEanJzT8EFNgM6EyYiB5UY6G779u2euKFLO1kzz40x\nOjJUmKghGmUS0VH7/WA+ikVgaUSkO1qOHC+vBYb5aS6ohI7EhbdkNjuPW4++KfVg\n3mVFMNNP4hlwSRr2LtEGhwIfctqjcYp/euI9j5eBXTB3AgnvMIJLJSOqiQKBgHjt\n+RNlPql2XwzxLpeJvN0mLqNORSNPs9mr0kbpV793OQ8sYmce9LdmhrdHg1v0Sfgz\nrFOfEHUGxgcm9cGqyUEeDQWEfYjyZ8M5GqH1gPH9UqcNlpgEqFV/wXOJ4bszAZwb\n+QRxSWX2uRSIZ64LKIZmxe5kJC6UEJ4Hk2hFYhSRAoGALbF7KG6GQe0PdRN13FsP\nmX007O8o/sDV6srFaifA1ff2F4syVl6VU9NfeHSDuyq6sG0Th/3pLPunpIfHVw1A\n7n2YyEkiCdrWcikgwYjLXBf8JAuVRTIka5Mo/h/7mIhAlehL1hs41vVR/2v6MpKt\nEiTZBMmusFhHbDB7lvYOsIE=\n-----END PRIVATE KEY-----\n",
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
        "private_key_id": "bae60fb003764ede6e466a09164f45e6c8b859c2",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC4uhgiRMWUC/1B\n0zEbwhqXdPHSkgVP7zhZ56lHbs6C251deRGpHoXfYiIYAzGpKKa9BREgMOkmrO+2\np9z5jFhJG1GcUCUYLMhO1QQSxCghbaeN2f6p+4nlhO7S+YMnHS8MHoQOauHpbUsd\n4IBrLUoQnADtyPS6TKNBjwCXPeEAOQXS78wuHw8achGt23ORnvnx7E8wAzIdUvOQ\nwusn5zLpkmIDGZW77Wu5nV9l3xlcZhfyQuwlM+/6scoi+zDarMm+Z69Xlnj7I0Cc\n2gsTaxVSzQpr49nLYQj2BAZsKpvAwuEq0JppLqU6VtS8VvMQeXPp6EN4znHHLl2w\nP244wQTjAgMBAAECggEAQFPdr6FPRHzgVpna0hXH+NIqm+9plipx7yzzEAMQOxWL\nOU+9zKzqZZ3gzYffNU8IsW4gRpuBtYwnde4Cz4wF+n9e7hYitMZzgrA/WOGiL/Hl\nlUpCmqMTpC+kkyd8epR5G7lMt1CVFxqOO/s//RKqZhpNYIDIaE/j0iKgTAqqXc7m\nJ/mPDoMXepY0IkDyipnWsOTBgkzfO5aR1GawyCTgGEdM/pGqFHoDI0PO3YoNtrcR\nsZikGTgQ2wWlsKkBUyYgR+gHi2Qas70nJtNOAFOkLgcEHnp3w96TMVAN2Uy4HDiR\nfOH9ZRQ/7e57s1F/WHYd98RHJQ4sks5eZlJKnO+ogQKBgQDgEk9x1OfVsp8XN5lZ\nTBd/795fMdKx0e3lJb1FuchrTyyvoCbKwyiER2oWaoKo4+qi3e9lTXrcFS+CVYvv\nafPunh1VnVy67+tcs3aXKc+0xM9Z+zk0wN/iuGZgYaLPuVQpsGTaZb1gkluSrSpa\nZUmuVybAZLrA12WAgnQwmjndYQKBgQDTDJIBdlWCytqCHkIMgHuYIRwoC30kgoS9\nh+Owhp9fHNxQ7rr384p3cFPhhXUgK0ECymafNUXgMfuCLG/WzrTS+2eWu7uMGzz5\nEVEXk4ehDrqnP2TTaMr4KVfufUbJ16OwFLsv/pQCBhEuQHjGxaSVVyULLG0NSdk6\nRjeiOWPkwwKBgC2FSsJzYE3Xpd5Pm0W64aNKFcD9HDKn1U6SJit+HKtAQHHFdVwH\n3blR0MmRBc5NzyMbN0E7RlRjsW0m9/DBc57sXEVCXM5VY1lH1DXNdrbgrMc49Fw1\nOsaSc6ns6+iLW//EKBj+RkTSNuxLZalLnnZemi7Hx/DZUXOUDQq6qjrBAoGAem7J\naMXAN578gg2RnXUPviI/FlAL6hk5bkYd5XNDk0bH3L+RgXQsOLvWPXdRijbtgPPv\n8p5SCgyU7mBfBQtnRRoJbx07YL0QcyEDnRy9ysYjrBCPqkEZtjstwrG0VjWdxPFR\n4jbaoA3q+5z1M8LGhshGOiQso0/bD/5aGecXN0cCgYEAxRp49NS00rx+SDLJYZbz\ntNnqNf+rY+dfoYKU38S295sFiDLc9D67KfSevSNgPn8nWFS3/OCzd3UQnZjQU0l3\nmutoYSXEZPJyNtWm9hUOEJdC65sH6pL1FYkqS+pSkehlsOBwSvQdMSJGSYB1/i9H\naBIUGqmmq0aBs0fnltDa1ek=\n-----END PRIVATE KEY-----\n",
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
