from time import sleep
from requests import get, Session
from TLBOT.config import token, user
from bs4 import BeautifulSoup


def login():
    key = token["rucaptcha"]
    captcha = get(f"http://rucaptcha.com/in.php?key={key}&method=userrecaptcha&googlekey="
                  f"6LeriWUUAAAAAJMt8OpbkWrWxVePsE_TRUVEX2sp&pageurl=https://cp.vimeworld.ru/login&json=1").json()
    print("Запуск решения капчи.")
    sleep(15)
    answer = get(f"http://rucaptcha.com/res.php?key={key}&action=get&id={captcha['request']}&json=1").json()
    while answer["request"] == "CAPCHA_NOT_READY":
        sleep(5)
        answer = get(f"http://rucaptcha.com/res.php?key={key}&action=get&id={captcha['request']}&json=1").json()
    else:
        print("Капча решена.")
    data = {
        "username": user["login"],
        "password": user["password"],
        "g-recaptcha-response": answer["request"],
        "login": "Войти",
        "remember": "true",
        "server": "lobby"
    }
    session = Session()
    session.post(url="https://cp.vimeworld.ru/login", data=data)
    account = session.get(url="https://cp.vimeworld.ru/index")
    if "MineCup" in account.text:
        print("Сессия авторизована.")
        send_vimers = {"usrnm": "FQGM",
                       "amount": 1,
                       "process": ""}
        payload = s.get("https://cp.vimeworld.ru/real?paylog")  # просмотр транзакций
        soup = BeautifulSoup(payload.text, 'lxml')
        vims = 0
        for tag in soup.find_all("b"):
            if "." in tag.text:
                vims = tag.text[:-3]
                break
        print(vims)
        send_vim = s.post("https://cp.vimeworld.ru/real?give", data=send_vimers)  # отправка вимеров
    return session
