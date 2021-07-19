from time import time
from datetime import datetime
from random import randint
from bs4 import BeautifulSoup
from discord import Client, Intents, Embed, utils
from Cybernator import Paginator
from asyncio import sleep
from aiohttp import ClientSession
from TLBOT.config import token, channels, month, month_num, sheet, bw_ids, rolez, heroku
from TLBOT.rating import rating
import heroku3
from memory_profiler import memory_usage


def start(services, session):
    async def team_req(squads):
        async with ClientSession() as session:
            res_squads = ""
            for i in squads:
                if i != squads[-1]:
                    res_squads += i + ","
                else:
                    res_squads += i
            async with session.get(f"https://api.vimeworld.ru/user/name/{res_squads}") as response:
                global online, names
                idd = ""
                online = []
                names = []
                pip = await response.json()
                try:
                    for w in range(len(pip)):
                        if w + 1 != len(pip):
                            idd += str(pip[w]["id"]) + ","
                        else:
                            idd += str(pip[w]["id"])
                    async with session.get(f"https://api.vimeworld.ru/user/session/{idd}") as response2:
                        pip2 = await response2.json()
                        checknames = []
                        for w2 in range(len(pip2)):
                            online.append(pip2[w2]["online"]["value"])
                            names.append(pip2[w2]["username"])
                            checknames.append(pip2[w2]["username"].upper())
                        if len(squads) > len(names):
                            for sq in range(len(squads)):
                                if squads[sq].upper() not in checknames:
                                    names.append(squads[sq])
                except:
                    names = "Извините, но эта команда добавила лишний симвов, из-за которого показ участников команды временно невозможен."

    class MyClient(Client):
        def __init__(self):
            intents = Intents.default()
            intents.members = True
            intents.guilds = True
            super().__init__(intents=intents)

        async def on_ready(self):
            print("Discordo!")
            guild = client.get_guild(856327254178791424)
            for channel in channels:
                channels[channel] = guild.get_channel(channels[channel])
            for role in rolez:
                rolez[role] = guild.get_role(rolez[role])
            messages = await channels["rating"].history(limit=100).flatten()
            if len(messages) > 1:
                await channels["rating"].purge(limit=len(messages) - 1)
            while True:
                await rating(services)
                print(f"MiB: {memory_usage()[0]}")
                if round(memory_usage()[0]) > 470:
                    heroku_conn = heroku3.from_key(heroku)
                    app = heroku_conn.apps()["team-league"]
                    app.restart()

        async def on_message(self, message):
            if message.author == self.user:
                return

            if message.content.startswith("*addteam"):
                if rolez["org2"] in message.author.roles or rolez["org"] in message.author.roles:
                    await message.delete()
                    wait = await message.channel.send("Идет процесс создания роли и комнаты...")
                    team = message.content.split()
                    perm_roles = [rolez["ss"], rolez["helper2"], rolez["org"], rolez["org2"]]
                    if len(team) > 1:
                        created_role = await message.guild.create_role(name=team[1],
                                                                       colour=0x787d85)
                        await sleep(.2)
                        if len(team) > 2:
                            category = message.guild.get_channel(int(team[2]))
                            chan = await message.guild.create_voice_channel(name=team[1],
                                                                            category=category)
                            await chan.set_permissions(message.guild.default_role,
                                                       connect=False,
                                                       view_channel=True)
                            perm_roles.append(created_role)
                            for perm in perm_roles:
                                await chan.set_permissions(perm,
                                                           connect=True,
                                                           view_channel=True)
                            await wait.edit(content="Создание роли и комнаты завершено.")
                        else:
                            chan = await message.guild.create_voice_channel(name=team[1])
                            await chan.set_permissions(message.guild.default_role,
                                                       connect=False,
                                                       view_channel=True)
                            perm_roles.append(created_role)
                            for perm in perm_roles:
                                await chan.set_permissions(perm,
                                                           connect=True,
                                                           view_channel=True)
                            await wait.edit(content="Создание роли и комнаты завершено.")
                    else:
                        await wait.edit(content="*addteam {название команды}' {ID категории}")

            if message.content.startswith("/addplayer") and message.channel == channels["payload"]:
                start_time = round(time()) + 3500 * 3
                user_role = message.author.roles[1]
                if user_role.name == "BedWars":
                    await message.channel.send(embed=Embed(title="══₪ Добавление игроков ₪══",
                                                           description=f"У вас нет командной роли.",
                                                           color=3553599))
                else:
                    addp = message.content.split(" ")
                    stop = False
                    mess = await message.channel.send(embed=Embed(title="══₪ Добавление игроков ₪══",
                                                                  description=f"⏲️ Ожидание перевода от {addp[2]}",
                                                                  color=3553599))
                    while start_time + 300 > round(time()) + 3500 * 3 and not stop:
                        payload = session.get("https://cp.vimeworld.ru/real?paylog")
                        soup = BeautifulSoup(payload.text, 'lxml')
                        payload_list = []
                        i = 0
                        for tag in soup.find_all("tr"):
                            if i != 0 and i < 10:
                                payload_list.append(tag.text.split("\n"))
                            else:
                                if i >= 10:
                                    break
                            i += 1

                        for ii in range(len(payload_list)):
                            timee = payload_list[ii][2].split()
                            for i in range(len(month)):
                                if str(timee[1]) == str(month[i]):
                                    timee[1] = month_num[i]
                                    break
                            if timee[3][1] == ":":
                                timee[3] = f"0{timee[3]}"
                            timee = f"{timee[2]}-{timee[1]}-{timee[0]} {timee[3]}:00"
                            dt = datetime.fromisoformat(timee)
                            payload_list[ii][2] = round(dt.timestamp())
                        for ww in range(len(payload_list)):
                            if round(start_time) < payload_list[ww][2]:
                                if addp[2].lower() in payload_list[ww][-2].lower() and payload_list[ww][-3] == "+30":
                                    stop = True
                                    break
                        await sleep(5)
                    if start_time + 300 < round(time()) + 3500 * 3:
                        await mess.edit(embed=Embed(title="══₪ Добавление игроков ₪══",
                                                    description=f"Время вышло.",
                                                    color=3553599))
                    else:
                        valuess = services["bot"].spreadsheets().values().get(
                            spreadsheetId=sheet["team_league"],
                            range=f'userlist!A2:B150',
                            majorDimension='ROWS'
                        ).execute()["values"]
                        for i in range(len(valuess)):
                            if valuess[i][0].lower() == user_role.name.lower():
                                services["bot"].spreadsheets().values().batchUpdate(spreadsheetId=sheet["team_league"],
                                                                                    body={
                                                                                        "valueInputOption": "USER_ENTERED",
                                                                                        "data": [
                                                                                            {
                                                                                                "range": f'userlist!B{i + 2}',
                                                                                                "majorDimension": "ROWS",
                                                                                                "values": [[
                                                                                                    f"{valuess[i][1]}, {addp[1]}"]]}]}).execute()
                        await mess.edit(embed=Embed(title="══₪ Добавление игроков ₪══",
                                                    description=f"Игрок {addp[1]} добавлен в команду <@&{user_role.id}>",
                                                    color=3553599))

            if message.channel == channels["roles"] and "@&" in message.content:
                role = message.guild.get_role(int(message.content[3:-1]))
                if str(role.color) == "#787d85":
                    valuess = services["bot"].spreadsheets().values().get(spreadsheetId=sheet["team_league"],
                                                                          range=f'userlist!A2:C150',
                                                                          majorDimension='ROWS'
                                                                          ).execute()["values"]
                    for value in valuess:
                        if value[0].lower() == role.name.lower():
                            if value[2] == "1":
                                emb = Embed(title="**══₪ TEAM LEAGUE ₪══**",
                                            description=f"Роль <@&{role.id}> не выдана. Команда заблокировала выдачу роли.",
                                            colour=3553599)
                                await message.channel.send(embed=emb)
                            else:
                                for author_role in message.author.roles:
                                    if author_role.color == "#787d85":
                                        await message.author.remove_roles(author_role)
                                await message.author.add_roles(role)
                                emb = Embed(title="**══₪ TEAM LEAGUE ₪══**",
                                            description=f"Роль <@&{role.id}> выдана.",
                                            colour=3553599)
                                await message.channel.send(embed=emb)
                else:
                    emb = Embed(title="**══₪ TEAM LEAGUE ₪══**",
                                description=f"Роль <@&{role.id}> не выдана.",
                                colour=3553599)
                    await message.channel.send(embed=emb)

            if message.content == "/close" and message.channel.id in bw_ids:
                role = message.guild.get_role(message.author.roles[1].id)
                if role.name != "BedWars" and str(role.color) == "#787d85":
                    valuess = services["bot"].spreadsheets().values().get(
                        spreadsheetId=sheet["team_league"],
                        range=f'userlist!A2:C150',
                        majorDimension='ROWS'
                    ).execute()["values"]
                    for i in range(len(valuess)):
                        if valuess[i][0].lower() == role.name.lower():
                            if valuess[i][2] == "1":
                                emb = Embed(title="**══₪ TEAM LEAGUE ₪══**",
                                            description=f"Ваша команда уже закрыта.",
                                            colour=3553599)
                                xx = await message.channel.send(embed=emb)
                                await sleep(6)
                                await xx.delete()
                            else:
                                services["bot"].spreadsheets().values().batchUpdate(
                                    spreadsheetId=sheet["team_league"],
                                    body={
                                        "valueInputOption": "USER_ENTERED",
                                        "data": [{"range": f'userlist!C{i + 2}',
                                                  "majorDimension": "ROWS",
                                                  "values": [["1"]]}]}).execute()
                                emb = Embed(title="**══₪ TEAM LEAGUE ₪══**",
                                            description=f"Ваша команда закрыта. Открыть - `/open`.",
                                            colour=3553599)
                                await message.channel.send(embed=emb)

            if message.content == "/open" and message.channel.id in bw_ids:
                role = message.guild.get_role(message.author.roles[1].id)
                if role.name != "BedWars" and str(role.color) == "#787d85":
                    valuess = services["bot"].spreadsheets().values().get(
                        spreadsheetId=sheet["team_league"],
                        range=f'userlist!A2:C150',
                        majorDimension='ROWS'
                    ).execute()["values"]
                    for i in range(len(valuess)):
                        if valuess[i][0].lower() == role.name.lower():
                            if valuess[i][2] == "0":
                                emb = Embed(title="**══₪ TEAM LEAGUE ₪══**",
                                            description=f"Ваша команда уже открыта.",
                                            colour=3553599)
                                await message.channel.send(embed=emb)
                            else:
                                services["bot"].spreadsheets().values().batchUpdate(
                                    spreadsheetId=sheet["team_league"],
                                    body={
                                        "valueInputOption": "USER_ENTERED",
                                        "data": [{"range": f'userlist!C{i + 2}',
                                                  "majorDimension": "ROWS",
                                                  "values": [["0"]]}]}).execute()
                                emb = Embed(title="**══₪ TEAM LEAGUE ₪══**",
                                            description=f"Ваша команда открыта. Закрыть - `/close`.",
                                            colour=3553599)
                                await message.channel.send(embed=emb)

            if message.content.startswith("/tl") and message.channel.id in bw_ids:
                valuess = services["bot"].spreadsheets().values().get(
                    spreadsheetId=sheet["team_league"],
                    range=f'helpers!A2:E100',
                    majorDimension='COLUMNS'
                ).execute()["values"]
                for i in range(len(valuess[0])):
                    if valuess[1][i].lower() == message.content[4:].lower():
                        name = f"═══₪ {valuess[1][i]} ₪═══"
                        vk_id = valuess[0][i]
                        discord = valuess[2][i]
                        games = valuess[3][i]
                        warns = valuess[4][i]
                        emb = Embed(title=name, url=f"https://vk.com/{vk_id[1:]}",
                                    description=f"""**Discord: <@{discord}>
        Проведено игр: `{games}`
        Предупреждений: `{warns}`**""", color=3553599)
                        emb.set_thumbnail(url=f"https://skin.vimeworld.ru/helm/3d/{valuess[1][i]}.png")
                        await message.channel.send(embed=emb)

            if message.content.startswith("/team"):
                team = ""
                if message.channel.id in bw_ids:
                    if message.content == "/team":
                        role = message.guild.get_role(message.author.roles[1].id)
                        if role.name != "@everyone" and str(role.color) == "#787d85":
                            team = role.name
                        else:
                            emb = Embed(colour=3553599)
                            emb.description = """**══₪ Просмотр команд ₪══**
        ⟫ `/team {название команды}` отправляет никнеймы участников команды.
        ⟫ `💚` аккаунт **в игре**
        ⟫ `💛` аккаунт **не в сети**
        ⟫ `🖤` аккаунт **не существует**"""
                            await message.channel.send(embed=emb)
                    else:
                        team = message.content[6:].lower()
                    if team != "":
                        valuess = services["bot"].spreadsheets().values().get(
                            spreadsheetId=sheet["team_league"],
                            range=f'userlist!A2:B250',
                            majorDimension='COLUMNS'
                        ).execute()["values"]
                        valuess1 = services["bot"].spreadsheets().values().get(
                            spreadsheetId=sheet["team_league"],
                            range=f'rate!A2:D250',
                            majorDimension='COLUMNS'
                        ).execute()["values"]
                        okk = False
                        for i in range(len(valuess[0])):
                            if valuess[0][i].lower() == team.lower():
                                okk = True
                                break
                            else:
                                if i == len(valuess[0]) - 1:
                                    squadnames = f"**══₪ TEAM LEAGUE ₪══**\n"
                                    emb = Embed(title=squadnames, description="Произошла ошибка в таблице [userlist]", color=3553599)
                                    await message.channel.send(embed=emb)
                                    break
                        if okk:
                            for ii in range(len(valuess1[0])):
                                if team.lower() == valuess1[0][ii].lower():
                                    ratingg = valuess1[2][ii]
                                    gamess = valuess1[3][ii]
                                    shitt = valuess1[1][ii]
                                    await team_req(valuess[1][i].split(", "))
                                    if names == "Извините, но эта команда добавила лишний симвов, из-за которого показ участников команды временно невозможен.":
                                        squadnames = f"**══₪ TEAM LEAGUE ₪══**\n"
                                        emb = Embed(title=squadnames, description=names, color=3553599)
                                        await message.channel.send(embed=emb)
                                        break
                                    else:
                                        squadnames = f"**══₪ `{valuess[0][i]}` ₪══**\n"
                                        names_x = []
                                        for nn in range(len(names)):
                                            if names[nn] != "":
                                                names_x.append(names[nn])
                                        for nn in range(len(names_x)):
                                            if len(online) >= nn + 1:
                                                if online[nn]:
                                                    if nn == 0:
                                                        squadnames += "`╔💚" + names_x[nn] + "`\n"
                                                    else:
                                                        if nn + 1 != len(names_x):
                                                            squadnames += "`║💚" + names_x[nn] + "`\n"
                                                        else:
                                                            squadnames += "`╚💚" + names_x[nn] + "`"
                                                else:
                                                    if nn == 0:
                                                        squadnames += "`╔💛" + names_x[nn] + "`\n"
                                                    else:
                                                        if nn + 1 != len(names_x):
                                                            squadnames += "`║💛" + names_x[nn] + "`\n"
                                                        else:
                                                            squadnames += "`╚💛" + names_x[nn] + "`"
                                            else:
                                                if nn == 0:
                                                    squadnames += "`╔🖤" + names_x[nn] + "`\n"
                                                else:

                                                    if nn + 1 != len(names_x):
                                                        squadnames += "`║🖤" + names_x[nn] + "`\n"
                                                    else:
                                                        squadnames += "`╚🖤" + names_x[nn] + "`"
                                        emb = Embed(description=squadnames, color=3553599)
                                        emb.set_footer(
                                            text=f"Рейтинг: {ratingg} [{ii + 1}/{len(valuess[0])}]\nИгр: {gamess}\nЗвание: {shitt}")
                                        await message.channel.send(embed=emb)
                                        break
                                else:
                                    if ii == len(valuess1[0]) - 1:
                                        squadnames = f"**══₪ TEAM LEAGUE ₪══**\n"
                                        emb = Embed(title=squadnames, description="Произошла ошибка в таблице [rate]", color=3553599)
                                        await message.channel.send(embed=emb)
                                        break

            if message.content.startswith("/check"):
                if message.channel.id in bw_ids:
                    for role in message.author.roles:
                        if role in rolez:
                            mes = message.content[7:].split(" ")
                            if mes != [""]:
                                valuess = services["bot"].spreadsheets().values().get(
                                    spreadsheetId=sheet["team_league"],
                                    range=f'userlist!A2:B250',
                                    majorDimension='COLUMNS'
                                ).execute()["values"]
                                desc = ""
                                footer = ""
                                blk = False
                                for i in range(len(mes)):
                                    for j in range(len(valuess[0])):
                                        if mes[i].lower() in valuess[1][j].lower():
                                            vv = valuess[1][j].split(", ")
                                            for v in vv:
                                                if mes[i].lower() == v.lower():
                                                    desc += f"**⟫ `{valuess[0][j]}` {mes[i]}**\n"
                                                    blk = True
                                                    break
                                            if blk:
                                                blk = False
                                                break

                                        else:
                                            if j + 1 == len(valuess[0]):
                                                if footer == "":
                                                    footer = "Не найдено: "
                                                footer += f"{mes[i]} "
                                emb = Embed(description="**══₪ Проверка игроков ₪══**\n" + desc,
                                            colour=3553599)
                                emb.set_footer(text=footer)
                                await message.channel.send(embed=emb)
                                break

            if message.channel == channels["rating"]:
                await message.delete()
                if message.content == "/rating":
                    table = services["bot"].spreadsheets().values().get(
                        spreadsheetId=sheet["team_league"],
                        range='rate!A2:D100',
                        majorDimension='COLUMNS'
                    ).execute()
                    try:
                        team = table["values"][0]
                        rating = table["values"][2]
                        games = table["values"][3]
                    except:
                        Embed(title="══₪ TEAM LEAGUE ₪══",
                              description="Произошла ошибка во время считывания таблицы.",
                              color=3553599)
                    oo = 0
                    teamm = []
                    ratingg = []
                    gamess = []
                    listt = []
                    if len(team) % 7 != 0:
                        for v in range(len(team) // 7 + 1):
                            teamm.append([])
                            ratingg.append([])
                            gamess.append([])
                            listt.append([])
                    else:
                        for v in range(len(team) // 7):
                            teamm.append([])
                            ratingg.append([])
                            gamess.append([])
                            listt.append([])
                    for ww in range(len(team)):
                        teamm[oo].append(team[ww])
                        ratingg[oo].append(rating[ww])
                        gamess[oo].append(games[ww])
                        if len(teamm[oo]) == 7:
                            oo += 1

                    for i in range(len(teamm)):
                        listt[i] = Embed(title="══₪ TEAM LEAGUE ₪══", color=3553599)
                        listt[i].add_field(
                            name=f"Команда",
                            value="_ _",
                            inline=True)
                        listt[i].add_field(
                            name=f"Игр",
                            value="_ _",
                            inline=True)
                        listt[i].add_field(
                            name=f"Рейтинг",
                            value="_ _",
                            inline=True)
                        for o in range(len(teamm[i])):
                            listt[i].add_field(
                                name=f"{teamm[i][o]}",
                                value="_ _",
                                inline=True)
                            listt[i].add_field(
                                name=f"`{gamess[i][o]}`",
                                value="_ _",
                                inline=True)
                            listt[i].add_field(
                                name=f"`{ratingg[i][o]}`",
                                value="_ _",
                                inline=True)
                    embs_all = await message.channel.send(embed=listt[0])
                    page = Paginator(client, embs_all, embeds=listt, only=message.author, timeout=300,
                                     use_remove_reaction=False, delete_message=True)
                    await page.start()

                elif message.content == "/prating":
                    table = services["bot"].spreadsheets().values().get(
                        spreadsheetId=sheet["team_league"],
                        range='rate!A2:D100',
                        majorDimension='COLUMNS'
                    ).execute()
                    try:
                        team = table["values"][0]
                        rating = table["values"][2]
                        games = table["values"][3]
                    except:
                        print("Пустые ячейки")
                    oo = 0
                    teamm = []
                    ratingg = []
                    gamess = []
                    listt = []
                    if len(team) % 7 != 0:
                        for v in range(len(team) // 7 + 1):
                            teamm.append([])
                            ratingg.append([])
                            gamess.append([])
                            listt.append([])
                    else:
                        for v in range(len(team) // 7):
                            teamm.append([])
                            ratingg.append([])
                            gamess.append([])
                            listt.append([])
                    for ww in range(len(team)):
                        teamm[oo].append(team[ww])
                        ratingg[oo].append(rating[ww])
                        gamess[oo].append(games[ww])
                        if len(teamm[oo]) == 7:
                            oo += 1

                    for i in range(len(teamm)):
                        desc = "**Команда Игр Рейтинг**\n"
                        for o in range(len(teamm[i])):
                            desc += f"**{teamm[i][o]} `{gamess[i][o]}` `{ratingg[i][o]}`**\n"
                        listt[i] = Embed(title="══₪ TEAM LEAGUE ₪══", description=desc, color=3553599)
                    embs_all = await message.channel.send(embed=listt[0])
                    page = Paginator(client, embs_all, embeds=listt, only=message.author, timeout=300,
                                     use_remove_reaction=False, delete_message=True)
                    await page.start()

            if message.content.startswith("/battle") and message.channel == channels["team_league"] and 1 == 2:
                now = datetime.now()
                mess = message.content.split()
                for role in message.author.roles:
                    for z in rolez:
                        if role == rolez[z] and role != rolez["ss"]:
                            if now.hour:
                                maps = await channels["map_pool"].fetch_message(858278776236015638)
                                maps = maps.content.split("\n")
                                mapp = maps[randint(0, len(maps) - 1)]
                                emb = Embed(title="════₪ TEAM LEAGUE ₪════",
                                            description=f"**{mess[1]} vs {mess[2]}**\n**Ведущий: <@{message.author.id}>**\n**Карта: {mapp}**",
                                            color=3553599)
                                mm = await message.channel.send(embed=emb)
                                emb = Embed(title="════₪ TEAM LEAGUE ₪════",
                                            url=f"https://discord.com/channels/856327254178791424/858273631033360384/{mm.id}",
                                            description=f"**{mess[1]} vs {mess[2]}**\n**Ведущий: <@{message.author.id}>**\n**Карта: {mapp}**\n**ID: `{mm.id}`**",
                                            color=3553599)
                                emb.set_footer(text="""1️⃣ - победила первая команда
2️⃣ - победила вторая команда
⏹️- отмена игры""")
                                m = await channels["match_logs"].send(embed=emb)
                                await sleep(0.2)
                                await m.add_reaction("1️⃣")
                                await m.add_reaction("2️⃣")
                                await m.add_reaction("⏹️")
                                break
                            else:
                                emb = Embed(title="══₪ TEAM LEAGUE ₪══",
                                            description=f"**Пользоваться `/battle` можно с 13:00 по 23:00 по мск.**",
                                            color=3553599)
                                await message.channel.send(embed=emb)
                                break

        async def on_raw_reaction_add(self, payload):
            if payload.channel_id == channels["match_logs"].id:
                channel = self.get_channel(payload.channel_id)
                message = await channel.fetch_message(payload.message_id)
                member = utils.get(message.guild.members, id=payload.user_id)
                mess = message.embeds[0].description
                if str(member.id) in mess or rolez["org2"] in member.roles:
                    emoji = str(payload.emoji)
                    mes = mess.split("\n")
                    mes[1] = mes[1].replace("**Ведущий: <@", "")
                    mes[1] = mes[1].replace(">**", "")
                    if emoji == "⏹️":
                        emb = Embed(title="════₪ TEAM LEAGUE ₪════",
                                    url=f"https://discord.com/channels/856327254178791424/858273631033360384/{mes[3][7:-3]}",
                                    description=f"**Отмена игры**\n**Написал команду: <@{mes[1]}>**\n{mes[3]}",
                                    color=3553599)
                        await message.edit(embed=emb)
                        await message.clear_reactions()
                    else:

                        mes[0] = mes[0].replace("**", "")
                        mes[0] = mes[0].replace("<@&", "")
                        mes[0] = mes[0].replace(">", "")
                        mes[0] = mes[0].split(" vs ")
                        team1 = mes[0][0]
                        team2 = mes[0][1]
                        role1 = client.get_guild(856327254178791424).get_role(int(team1))
                        role2 = client.get_guild(856327254178791424).get_role(int(team2))

                        if emoji == "1️⃣":
                            X = 1
                            valuess = services["bot"].spreadsheets().values().get(
                                spreadsheetId=sheet["team_league"],
                                range=f'matches!A{str(X)}:A1000',
                                majorDimension='COLUMNS'
                            ).execute()
                            try:
                                X += len(valuess["values"][0])
                            except:
                                pass
                            services["bot"].spreadsheets().values().batchUpdate(
                                spreadsheetId=sheet["team_league"],
                                body={
                                    "valueInputOption": "USER_ENTERED",
                                    "data": [{"range": f'matches!A{str(X)}:G{str(X)}',
                                              "majorDimension": "ROWS",
                                              "values": [[str(role1), str(role2), str(mes[1]), str(mes[3][7:-3]),
                                                          str(datetime.now())[:-7]]]}]}).execute()
                            emb = Embed(title="════₪ TEAM LEAGUE ₪════",
                                        url=f"https://discord.com/channels/856327254178791424/858273631033360384/{mes[3][7:-3]}",
                                        description=f"**Победитель: <@&{team1}>**\n**Проигравший: <@&{team2}>**\n**Провел игру"
                                                    f": <@{mes[1]}>**\n{mes[3]}",
                                        color=3553599)
                            await message.edit(embed=emb)
                            await message.clear_reactions()
                        elif emoji == "2️⃣":
                            X = 2
                            valuess = services["bot"].spreadsheets().values().get(
                                spreadsheetId=sheet["team_league"],
                                range=f'matches!A{str(X)}:A1000',
                                majorDimension='COLUMNS'
                            ).execute()
                            try:
                                X += len(valuess["values"][0])
                            except:
                                pass
                            services["bot"].spreadsheets().values().batchUpdate(
                                spreadsheetId=sheet["team_league"],
                                body={
                                    "valueInputOption": "USER_ENTERED",
                                    "data": [{"range": f'matches!A{str(X)}:G{str(X)}',
                                              "majorDimension": "ROWS",
                                              "values": [[str(role2), str(role1), str(mes[1]), str(mes[3][7:-3]),
                                                          str(datetime.now())[:-7]]]}]}).execute()
                            emb = Embed(title="════₪ TEAM LEAGUE ₪════",
                                        url=f"https://discord.com/channels/856327254178791424/858273631033360384/{mes[3][7:-3]}",
                                        description=f"**Победитель: <@&{team2}>**\n**Проигравший: <@&{team1}>**\n**Провел игру"
                                                    f": <@{mes[1]}>**\n{mes[3]}",
                                        color=3553599)
                            await message.edit(embed=emb)
                            await message.clear_reactions()

    client = MyClient()
    client.run(token["bot"])
