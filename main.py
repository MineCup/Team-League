from TLBOT.login import login
from TLBOT.table import table
from TLBOT.bot import start


def run():
    session = login()
    services = table()
    start(services, session)


if __name__ == "__main__":
    run()
