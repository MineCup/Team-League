from BOT.bot import start
from BOT.table import table
from BOT.login import login


def run():
    session = login()
    services = table()
    start(services, session)


if __name__ == "__main__":
    run()
