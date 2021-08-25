from time import time
from datetime import datetime
from random import randint
from aiohttp import ClientSession
from asyncio import sleep
from bs4 import BeautifulSoup
from Cybernator import Paginator
from discord import Client, Embed, Intents, utils
from BOT.config_for_git import token, channels, rolez


def start(services, session):
    sheet = "1OaMpmMMFR_NIzmqtEh12XJ6N4X9R723S4g709FKvj_8"

    bw_ids = [858273631033360384, 856786815130533928]

    month = ["Янв.", "Фев.", "Марта", "Апр.", "Мая", "Июня", "Июля", "Авг.", "Сент.", "Окт.", "Нояб.", "Дек."]
    month_num = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]

    async def teamSwitch(message, switch):
        switcher = ["открыта", "закрыта"]
        switcher2 = ["Закрыть: /close", "Открыть: /open"]
        role = message.guild.get_role(message.author.roles[1].id)
        if str(role.color) != "#787d85":
            emb = Embed(title="**══₪ TEAM LEAGUE ₪══**",
                        description=f"У вас нет командной роли.",
                        colour=3553599)
            await message.channel.send(embed=emb)
            return

        teams = services["bot"].spreadsheets().values().get(spreadsheetId=sheet,
                                                            range=f'userlist!A2:C150',
                                                            majorDimension='ROWS'
                                                            ).execute()["values"]
        for i in range(len(teams)):
            if teams[i][0].lower() == role.name.lower():
                if teams[i][2] == switch:
                    emb = Embed(title="**══₪ TEAM LEAGUE ₪══**",
                                description=f"Ваша команда уже {switcher[int(switch)]}.",
                                colour=3553599)
                    await message.channel.send(embed=emb)
                else:
                    services["bot"].spreadsheets().values().batchUpdate(spreadsheetId=sheet,
                                                                        body={"valueInputOption": "USER_ENTERED",
                                                                              "data": [{"range": f'userlist!C{i + 2}',
                                                                                        "majorDimension": "ROWS",
                                                                                        "values": [
                                                                                            [switch]]}]}).execute()
                    emb = Embed(title="**══₪ TEAM LEAGUE ₪══**",
                                description=f"Ваша команда {switcher[int(switch)]}. {switcher2[int(switch)]}",
                                colour=3553599)
                    await message.channel.send(embed=emb)

    async def helperVariant(message, variant, helpers, answer):
        for helper in helpers:
            if variant == helper[2] or variant == helper[1]:
                name = f"═══₪ {helper[1]} ₪═══"
                vk_id = helper[0]
                discord = helper[2]
                games = helper[3]
                warns = helper[4]
                emb = Embed(title=name,
                            url=f"https://vk.com/{vk_id[1:]}",
                            description=f"""**Discord: <@{discord}>
                Проведено игр: `{games}`
                Предупреждений: `{warns}`**""", color=3553599)
                emb.set_thumbnail(url=f"https://skin.vimeworld.ru/helm/3d/{helper[1]}.png")
                await message.channel.send(embed=emb)
                return
        await message.channel.send(answer)

    async def membersStatusCheck(members):
        async with ClientSession() as session:
            userIDs = ""
            members = members.replace(" ", "")

            async with session.get(f"https://api.vimeworld.ru/user/name/{members}") as response:
                answer = await response.json()
                if "error" in answer:
                    return "error"

                for user in answer:
                    userIDs += str(user["id"]) + ","
                userIDs = userIDs[:-1]

            async with session.get(f"https://api.vimeworld.ru/user/session/{userIDs}") as response:
                answer = await response.json()
                members = {"Nickname": [],
                           "Session": []}

                for user in answer:
                    members["Nickname"].append(user["username"])
                    members["Session"].append(user["online"]["value"])
                return members

    async def checkTeam(message, name):
        userList = services["bot"].spreadsheets().values().get(spreadsheetId=sheet,
                                                               range=f'userlist!A2:D250',
                                                               majorDimension='ROWS'
                                                               ).execute()["values"]
        rating = services["bot"].spreadsheets().values().get(spreadsheetId=sheet,
                                                             range=f'rate!A2:D250',
                                                             majorDimension='ROWS'
                                                             ).execute()["values"]

        team = {"Name": None,
                "Members": None,
                "Block": None,
                "Warnings": None,
                "Rating": None,
                "Position": None,
                "Games": None,
                "Rank": None}

        for users in userList:
            if users[0].lower() == name.lower():
                team["Name"] = users[0]
                team["Members"] = users[1]
                if users[2] == "1":
                    team["Block"] = "Команда закрыта"
                else:
                    team["Block"] = "Команда открыта"
                team["Warnings"] = users[3]
                break

        for num, rate in enumerate(rating):
            if rate[0].lower() == name.lower():
                team["Rating"] = rate[2]
                team["Position"] = num + 1
                team["Games"] = rate[3]
                team["Rank"] = rate[1]
                break

        if not team["Name"]:
            emb = Embed(title="**══₪ TEAM LEAGUE ₪══**", description="Произошла ошибка в таблице [userlist]",
                        color=3553599)
            await message.channel.send(embed=emb)
            return

        if not team["Position"]:
            emb = Embed(title="**══₪ TEAM LEAGUE ₪══**", description="Произошла ошибка в таблице [rate]",
                        color=3553599)
            await message.channel.send(embed=emb)
            return

        answer = await membersStatusCheck(team["Members"])
        if answer == "error":
            emb = Embed(title="**══₪ TEAM LEAGUE ₪══**", description="Произошла ошибка в составе игроков. [userlist]",
                        color=3553599)
            await message.channel.send(embed=emb)
            return

        team["Members"] = answer
        nicknames = ""
        for i in range(len(team["Members"]["Nickname"])):
            if team["Members"]["Session"][i]:
                nicknames += f'🟢 **{team["Members"]["Nickname"][i]}**\n'
            else:
                nicknames += f'🔴 **{team["Members"]["Nickname"][i]}**\n'
        emb = Embed(title=f'**══₪ {team["Name"]} ₪══**',
                    description=nicknames, color=3553599)
        emb.set_footer(text=f'Рейтинг: {team["Rating"]} [{team["Position"]}/{len(rating) + 1}]\n'
                            f'Игр: {team["Games"]}\n'
                            f'Звание: {team["Rank"]}\n'
                            f'Предупреждений: {team["Warnings"]}\n'
                            f'{team["Block"]}')
        await message.channel.send(embed=emb)

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
            try:
                messages = await channels["rating"].history(limit=100).flatten()
                if len(messages) > 1:
                    await channels["rating"].purge(limit=len(messages) - 1)
            except:
                pass

        async def on_message(self, message):
            if message.author == self.user:
                return

            if message.content.startswith("*addteam"):
                await message.delete()
                userRoles = message.author.roles
                if rolez["org2"] not in userRoles and rolez["org"] not in userRoles and rolez["tech"] not in userRoles:
                    dell = await message.channel.send(
                        f"<@{message.author.id}>, Данная команда доступна для Организатор и выше.")
                    await dell.delete(delay=10)
                    return

                info = message.content.split()

                if len(info) <= 1 or len(info) > 3:
                    dell = await message.channel.send(f"Некорректная команда: `{message.content}`. \n"
                                                      f"Попробуйте *addteam (название команды) (цифровой id категории / не обязательно)")
                    await dell.delete(delay=10)
                    return

                wait = await message.channel.send("Идет процесс создания роли...")

                permRoles = [rolez["ss"], rolez["helper2"], rolez["org"], rolez["org2"],
                             await message.guild.create_role(name=info[1],
                                                             colour=0x787d85,
                                                             mentionable=True)]
                await wait.edit(content=f"Создание роли завершено. \nИдет процесс создания комнаты...")

                category = None
                if len(info) > 2:
                    category = message.guild.get_channel(int(info[2]))

                chan = await message.guild.create_voice_channel(name=info[1], category=category)
                await chan.set_permissions(message.guild.default_role, connect=False, view_channel=True)
                for perm in permRoles:
                    await chan.set_permissions(perm, connect=True, view_channel=True)

                await wait.edit(
                    content=f"Создание комнаты <#{chan.id}> для команды <@&{permRoles[-1].id}> успешно завершено.")
                return

            if message.channel == channels["roles"]:
                if "@&" in message.content:
                    removed = "Убраны роли:"
                    try:
                        role = message.guild.get_role(int(message.content[3:-1]))
                    except ValueError:
                        emb = Embed(title="**══₪ TEAM LEAGUE ₪══**",
                                    description=f"Проблема с пингом роли: `{message.content}`",
                                    colour=3553599)
                        await message.channel.send(embed=emb)
                        return
                    if not role:
                        emb = Embed(title="**══₪ TEAM LEAGUE ₪══**",
                                    description=f"Вы пинганули неизвестную роль: `{message.content}`",
                                    colour=3553599)
                        await message.channel.send(embed=emb)
                        return

                    if str(role.color) != "#787d85":
                        emb = Embed(title="**══₪ TEAM LEAGUE ₪══**",
                                    description=f"Роль <@&{role.id}> не выдана. Это не командная роль.",
                                    colour=3553599)
                        await message.channel.send(embed=emb)
                        return

                    teams = services["bot"].spreadsheets().values().get(spreadsheetId=sheet,
                                                                        range=f'userlist!A2:C150',
                                                                        majorDimension='ROWS'
                                                                        ).execute()["values"]
                    for team in teams:
                        if team[0].lower() == role.name.lower():
                            if team[2] == "1":
                                emb = Embed(title="**══₪ TEAM LEAGUE ₪══**",
                                            description=f"Роль <@&{role.id}> не выдана. Команда заблокировала выдачу роли.",
                                            colour=3553599)
                                await message.channel.send(embed=emb)
                                break
                            else:
                                for authorRole in message.author.roles:
                                    if str(authorRole.color) == "#787d85":
                                        await message.author.remove_roles(authorRole)
                                        removed += f" {authorRole.name}"
                                await message.author.add_roles(role)
                                emb = Embed(title="**══₪ TEAM LEAGUE ₪══**",
                                            description=f"Роль <@&{role.id}> выдана.",
                                            colour=3553599)
                                if removed != "Убраны роли:":
                                    emb.set_footer(text=removed)
                                await message.channel.send(embed=emb)
                                break

                else:
                    if "/close" == message.content:
                        await teamSwitch(message, "1")
                    elif "/open" == message.content:
                        await teamSwitch(message, "0")
                    else:
                        return

            if message.content.startswith("/tl") and message.channel.id in bw_ids:
                answerVariant = [f"Вы не помощник Team League.",
                                 f"Помощник с идентификатором {message.content[4:]} не обнаружен."]
                helpers = services["bot"].spreadsheets().values().get(
                    spreadsheetId=sheet,
                    range=f'helpers!A2:E159',
                    majorDimension='ROWS'
                ).execute()["values"]

                if message.content == "/tl":
                    await helperVariant(message, str(message.author.id), helpers, answerVariant[0])

                else:
                    await helperVariant(message, message.content[4:], helpers, answerVariant[1])

            if message.content.startswith("/team") and message.channel.id in bw_ids:
                if message.content == "/team":
                    role = message.guild.get_role(message.author.roles[1].id)
                    if str(role.color) == "#787d85":
                        await checkTeam(message, role.name)
                    else:
                        emb = Embed(colour=3553599)
                        emb.description = """**══₪ Просмотр команд ₪══**
    ⟫ `/team {название команды}` отправляет никнеймы участников команды.
    ⟫ `💚` аккаунт **в игре**
    ⟫ `💛` аккаунт **не в сети**"""
                        await message.channel.send(embed=emb)
                        return
                else:
                    await checkTeam(message, message.content[6:].lower())

            if message.channel == channels["rating"]:
                await message.delete()
                if message.content == "/rating":
                    table = services["bot"].spreadsheets().values().get(
                        spreadsheetId=sheet,
                        range='rate!A2:D100',
                        majorDimension='COLUMNS'
                    ).execute()
                    try:
                        team = table["values"][0]
                        rating = table["values"][2]
                        games = table["values"][3]
                    except:
                        return
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
                        spreadsheetId=sheet,
                        range='rate!A2:D100',
                        majorDimension='COLUMNS'
                    ).execute()
                    try:
                        team = table["values"][0]
                        rating = table["values"][2]
                        games = table["values"][3]
                    except:
                        return
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

            if message.content.startswith("/battle") and message.channel == channels["team_league"]:
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

        async def on_raw_reaction_add(self, payload):
            try:
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
                                                  "values": [
                                                      [str(role1), str(role2), str(mes[1]), str(mes[3][7:-3]),
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
                                                  "values": [
                                                      [str(role2), str(role1), str(mes[1]), str(mes[3][7:-3]),
                                                       str(datetime.now())[:-7]]]}]}).execute()
                                emb = Embed(title="════₪ TEAM LEAGUE ₪════",
                                            url=f"https://discord.com/channels/856327254178791424/858273631033360384/{mes[3][7:-3]}",
                                            description=f"**Победитель: <@&{team2}>**\n**Проигравший: <@&{team1}>**\n**Провел игру"
                                                        f": <@{mes[1]}>**\n{mes[3]}",
                                            color=3553599)
                                await message.edit(embed=emb)
                                await message.clear_reactions()
            except:
                pass

    client = MyClient()
    client.run(token["bot"])
