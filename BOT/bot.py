from time import time
from datetime import datetime
from random import choice
from regexp import re
from aiohttp import ClientSession
from asyncio import sleep
from bs4 import BeautifulSoup
from Cybernator import Paginator
from discord import Client, Embed, Intents
from memory_profiler import memory_usage
from BOT.config import token, channels, minecupRoles


def start(services, session):
    sheet = "1OaMpmMMFR_NIzmqtEh12XJ6N4X9R723S4g709FKvj_8"

    bw_ids = [815244363633786910, 815487803709980682]

    month = ["Янв.", "Фев.", "Марта", "Апр.", "Мая", "Июня", "Июля", "Авг.", "Сент.", "Окт.", "Нояб.", "Дек."]
    month_num = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]

    async def ratingShow(message, prating, pages):
        if prating:  # /prating
            for num, page in enumerate(pages):
                desc = "**Команда Рейтинг Игр**\n"
                for team in page:
                    desc += f"**{team[0]} {team[2]} {team[3]}**\n"
                pages[num] = Embed(title="══₪ TEAM LEAGUE ₪══", description=desc, color=3553599)
            embeds = await message.channel.send(embed=pages[0])
            page = Paginator(client, embeds, embeds=pages, only=message.author, timeout=300,
                             use_remove_reaction=False, delete_message=True, use_exit=True)
            await page.start()
            return

        else:  # /rating
            for num, page in enumerate(pages):
                pages[num] = Embed(title="══₪ TEAM LEAGUE ₪══", color=3553599)
                pages[num].add_field(name=f"Команда",
                                     value="_ _",
                                     inline=True)
                pages[num].add_field(name=f"Рейтинг",
                                     value="_ _",
                                     inline=True)
                pages[num].add_field(name=f"Игр",
                                     value="_ _",
                                     inline=True)
                for team in page:
                    for i in range(3):
                        if i > 0:
                            i += 1
                        pages[num].add_field(name=team[i],
                                             value="_ _",
                                             inline=True)
            embeds = await message.channel.send(embed=pages[0])
            page = Paginator(client, embeds, embeds=pages, only=message.author, timeout=300,
                             use_remove_reaction=False, delete_message=True, use_exit=True)
            await page.start()
            return

    async def teamSwitch(message, switch):
        switcher = ["открыта", "закрыта"]
        switcher2 = ["Закрыть: /close", "Открыть: /open"]
        try:
            role = message.guild.get_role(message.author.roles[1].id)
        except:
            role = message.guild.get_role(message.author.roles[0].id)
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
                    return
                else:
                    del teams
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
                    return

    async def helperVariant(message, variant, helpers, answer):
        for helper in helpers:
            if variant == helper[2].replace(" ", "") or variant.lower() == helper[1].lower().replace(" ", ""):
                emb = Embed(title=f"═══₪ {helper[1]} ₪═══",
                            url=f"https://vk.com/{helper[0][1:]}",
                            description=f"""**Discord: <@{helper[2]}>
                Проведено игр: `{helper[3]}`
                Предупреждений: `{helper[4]}`**""", color=3553599)
                emb.set_thumbnail(url=f"https://skin.vimeworld.ru/helm/3d/{helper[1].replace(' ', '')}.png")
                await message.channel.send(embed=emb)
                return
        await message.channel.send(answer)
        return

    async def membersStatusCheck(members):
        async with ClientSession() as s:
            userIDs = ""
            members = members.replace(" ", "")

            async with s.get(f"https://api.vimeworld.ru/user/name/{members}") as response:
                answer = await response.json()
                if "error" in answer:
                    return "error"

                for user in answer:
                    userIDs += str(user["id"]) + ","
                userIDs = userIDs[:-1]

            async with s.get(f"https://api.vimeworld.ru/user/session/{userIDs}") as response:
                answer = await response.json()
                if "error" in answer:
                    return "error"

                members = {"Nickname": [],
                           "Session": []}

                for user in answer:
                    members["Nickname"].append(user["username"])
                    members["Session"].append(user["online"]["value"])
                return members

    async def checkTeam(message, name):
        if " " == name[0]:
            name = name[1:]
        
        userList = services["bot"].spreadsheets().values().get(spreadsheetId=sheet,
                                                               range=f'userlist!A2:D250',
                                                               majorDimension='ROWS'
                                                               ).execute()
        if "values" not in userList:
            emb = Embed(title="**══₪ TEAM LEAGUE ₪══**",
                        description="UserListSheet: Произошла критическая ошибка в таблице.",
                        color=3553599)
            await message.channel.send(embed=emb)
            return

        rateList = services["bot"].spreadsheets().values().get(spreadsheetId=sheet,
                                                               range=f'rate!A2:D250',
                                                               majorDimension='ROWS'
                                                               ).execute()
        if "values" not in rateList:
            emb = Embed(title="**══₪ TEAM LEAGUE ₪══**",
                        description="RateSheet: Произошла критическая ошибка в таблице.",
                        color=3553599)
            await message.channel.send(embed=emb)
            return

        team = {"Name": None,
                "Members": None,
                "Block": None,
                "Warnings": None,
                "Rating": None,
                "Position": None,
                "Games": None,
                "Rank": None}

        for users in userList["values"]:
            if users[0].lower() == name.lower():
                team["Name"] = users[0]
                team["Members"] = users[1]
                if users[2] == "1":
                    team["Block"] = "Команда закрыта"
                else:
                    team["Block"] = "Команда открыта"
                team["Warnings"] = users[3]
                del userList
                break

        for num, rate in enumerate(rateList["values"]):
            if rate[0].lower() == name.lower():
                team["Rating"] = rate[2]
                team["Position"] = num + 1
                team["Games"] = rate[3]
                team["Rank"] = rate[1]
                break

        if not team["Name"]:
            emb = Embed(title="**══₪ TEAM LEAGUE ₪══**",
                        description="UserListSheet: Ваша команда удалена или еще не добавлена.",
                        color=3553599)
            await message.channel.send(embed=emb)
            return

        if not team["Position"]:
            emb = Embed(title="**══₪ TEAM LEAGUE ₪══**",
                        description="RateSheet: Ваша команда удалена или еще не добавлена.",
                        color=3553599)
            await message.channel.send(embed=emb)
            return

        answer = await membersStatusCheck(team["Members"])
        if answer == "error":
            emb = Embed(title="**══₪ TEAM LEAGUE ₪══**",
                        description="UserListSheet: Произошла ошибка в проверке состава игроков.",
                        color=3553599)
            await message.channel.send(embed=emb)
            return

        team["Members"] = answer
        nicknames = ""
        for i in range(len(team["Members"]["Nickname"])):
            if team["Members"]["Session"][i]:
                nicknames += f'🟢 **`{team["Members"]["Nickname"][i]}`**\n'
            else:
                nicknames += f'🔴 **`{team["Members"]["Nickname"][i]}`**\n'
        emb = Embed(title=f'**══₪ {team["Name"]} ₪══**',
                    description=nicknames, color=3553599)
        emb.set_footer(text=f'Рейтинг: {team["Rating"]} [{team["Position"]}/{len(rateList["values"])}]\n'
                            f'Игр: {team["Games"]}\n'
                            f'Звание: {team["Rank"]}\n'
                            f'Предупреждений: {team["Warnings"]}\n'
                            f'{team["Block"]}')
        await message.channel.send(embed=emb)
        return

    async def infoToSheet(message, message_id, winner, loser, length, author, mention):
        services["bot"].spreadsheets().values().batchUpdate(
            spreadsheetId=sheet,
            body={
                "valueInputOption": "USER_ENTERED",
                "data": [{
                    "range": f'matches!A{str(length)}:G{str(length)}',
                    "majorDimension": "ROWS",
                    "values": [[winner.name,
                                loser.name,
                                author[0],
                                message_id,
                                str(datetime.now())[:-7]]]
                }]}).execute()
        emb = Embed(title="════₪ TEAM LEAGUE ₪════",
                    url=f"https://discord.com/channels/856327254178791424/858273631033360384/{message_id}",
                    description=f"**Победитель: {winner.mention}**\n"
                                f"**Проигравший: {loser.mention}**\n"
                                f"**Провел матч: <@{author[0]}>**\n"
                                f"**Отметил матч: {mention}**\n"
                                f"**ID: `{message_id}`**",
                    color=3553599)
        await message.edit(embed=emb)
        await message.clear_reactions()

    class MyClient(Client):
        def __init__(self):
            intents = Intents.default()
            intents.members = True
            intents.guilds = True
            super().__init__(intents=intents)

        async def on_ready(self):
            print("Discordo!")
            guild = client.get_guild(582587958717054987)
            for channel in channels:
                channels[channel] = guild.get_channel(channels[channel])
            for role in minecupRoles:
                minecupRoles[role] = guild.get_role(minecupRoles[role])
            try:
                messages = await channels["rating"].history(limit=100).flatten()
                if len(messages) > 1:
                    await channels["rating"].purge(limit=len(messages) - 1)
            except:
                return

        async def on_message(self, message):
            if message.author.bot:
                return

            if message.guild:
                if minecupRoles["tech"] in message.author.roles and message.content == "*status":
                    await message.channel.send(f"MiB: {memory_usage()[0]}")
                    return

                if message.content.startswith("*addteam"):
                    if minecupRoles["org2"] not in message.author.roles and minecupRoles["org"] \
                            not in message.author.roles and minecupRoles["tech"] not in message.author.roles:
                        dell = await message.channel.send(
                            f"{message.author.mention}, Данная команда доступна для Организатор и выше.")
                        await dell.delete(delay=10)
                        return

                    info = message.content.split()

                    if len(info) <= 1 or len(info) > 3:
                        dell = await message.channel.send(f"Некорректная команда: `{message.content}`. \n"
                                                          f"Попробуйте *addteam (название команды) (цифровой id категории / не обязательно)")
                        await dell.delete(delay=10)
                        return

                    wait = await message.channel.send("Идет процесс создания роли...")

                    permRoles = [minecupRoles["ss"], minecupRoles["org"], minecupRoles["org2"],
                                 await message.guild.create_role(name=info[1],
                                                                 colour=0x787d85,
                                                                 mentionable=True)]
                    await wait.edit(content=f"Создание роли завершено. \nИдет процесс создания комнаты...")

                    category = None
                    if len(info) > 2:
                        category = message.guild.get_channel(int(info[2]))
                        if len(category.channels) == 50:
                            category = None

                    chan = await message.guild.create_voice_channel(name=info[1], category=category)
                    await chan.set_permissions(message.guild.default_role, connect=False, view_channel=True)
                    for perm in permRoles:
                        await chan.set_permissions(perm, connect=True, view_channel=True)

                    if not category:
                        await wait.edit(
                            content=f"Создание комнаты {chan.mention} для команды {permRoles[-1].mention} успешно завершено.")
                    else:
                        await wait.edit(
                            content=f"Создание комнаты {chan.mention} для команды {permRoles[-1].mention} успешно завершено.\n"
                                    f"В категории {category.mention} находится {len(category.channels)} каналов.")
                    return

                if message.channel == channels["roles"]:
                    if "@&" in message.content:
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
                                        description=f"Роль {role.mention} не выдана. Это не командная роль.",
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
                                                description=f"Роль {role.mention} не выдана. Команда заблокировала выдачу роли.",
                                                colour=3553599)
                                    await message.channel.send(embed=emb)
                                    return
                                else:
                                    del teams, team
                                    removed = "Убраны роли:"
                                    for authorRole in message.author.roles:
                                        if str(authorRole.color) == "#787d85":
                                            await message.author.remove_roles(authorRole)
                                            removed += f" {authorRole.name}"
                                    await message.author.add_roles(role)
                                    emb = Embed(title="**══₪ TEAM LEAGUE ₪══**",
                                                description=f"Роль {role.mention} выдана.",
                                                colour=3553599)
                                    if removed != "Убраны роли:":
                                        emb.set_footer(text=removed)
                                    await message.channel.send(embed=emb)
                                    return

                    else:
                        if "/close" == message.content:
                            await teamSwitch(message, "1")
                        elif "/open" == message.content:
                            await teamSwitch(message, "0")
                        return

                if message.content.startswith("/tl") and message.channel.id in bw_ids:
                    answerVariant = [f"Вы не помощник Team League.",
                                     f"Помощник с идентификатором `{message.content[4:]}` не обнаружен."]

                    helpers = services["bot"].spreadsheets().values().get(
                        spreadsheetId=sheet,
                        range=f'helpers!A3:E159',
                        majorDimension='ROWS'
                    ).execute()

                    if "values" not in helpers:
                        return

                    if message.content == "/tl":
                        variant = re.search(r'\d+', str(message.author.id))[0]
                        await helperVariant(message, variant, helpers["values"], answerVariant[0])

                    else:
                        variant = re.search(r'\d+', str(message.content[4:]))
                        if variant is None:
                            await helperVariant(message, message.content[4:], helpers["values"], answerVariant[1])
                            return
                        if f"<@{variant}>" == message.content[4:] or f"<@!{variant}>" == message.content[4:]:
                            await helperVariant(message, variant, helpers["values"], answerVariant[1])
                        else:
                            await helperVariant(message, message.content[4:], helpers["values"], answerVariant[1])
                            
                    return

                if message.content.startswith("/team") and message.channel.id in bw_ids:
                    if message.content == "/team":
                        try:
                            role = message.guild.get_role(message.author.roles[1].id)
                        except:
                            emb = Embed(colour=3553599)
                            emb.description = """**══₪ Просмотр команд ₪══**
                                ⟫ `/team {название команды}` отправляет никнеймы участников команды.
                                ⟫ `💚` аккаунт **в игре**
                                ⟫ `💛` аккаунт **не в сети**"""
                            await message.channel.send(embed=emb)
                            return
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
                    return

                if message.channel == channels["rating"]:
                    await message.delete()

                    if "/prating" in message.content:
                        prating = True
                    elif "/rating" == message.content:
                        prating = False
                    else:
                        return

                    rateList = services["bot"].spreadsheets().values().get(spreadsheetId=sheet,
                                                                           range='rate!A2:D100',
                                                                           majorDimension='ROWS'
                                                                           ).execute()

                    if "values" not in rateList:
                        emb = Embed(title="**══₪ TEAM LEAGUE ₪══**",
                                    description="RateSheet: Произошла критическая ошибка в таблице.",
                                    color=3553599)
                        await message.channel.send(embed=emb)
                        return

                    ratePage = []
                    for i in range(1, len(rateList["values"]) + 1):
                        if i % 7 == 0:
                            ratePage.append([])
                    if len(rateList["values"]) % 7 != 0:
                        ratePage.append([])

                    ratePageNum = 0
                    for rate in rateList["values"]:
                        if len(ratePage[ratePageNum]) % 7 == 0 and len(ratePage[ratePageNum]):
                            ratePageNum += 1
                        ratePage[ratePageNum].append(rate)
                    del rateList, ratePageNum

                    await ratingShow(message, prating, ratePage)

                if message.content.startswith("/battle") and message.channel == channels["team_league"]:
                    for role in message.author.roles:
                        for minecupRole in minecupRoles:
                            if role == minecupRoles[minecupRole] and role != minecupRoles["ss"]:
                                now = datetime.now()
                                if 9 < now.hour < 20:
                                    del now

                                    mess = message.content.split()
                                    if len(mess) != 3:
                                        emb = Embed(title="══₪ TEAM LEAGUE ₪══",
                                                    description=f"**Ошибка в создании матча.**",
                                                    color=3553599)
                                        await message.channel.send(embed=emb)
                                        return

                                    first = re.search(r'\d+', mess[1])
                                    if not first:
                                        emb = Embed(title="══₪ TEAM LEAGUE ₪══",
                                                    description=f"**Ошибка в выборе команды. {mess[1]}**",
                                                    color=3553599)
                                        await message.channel.send(embed=emb)
                                        return
                                    try:
                                        checkRole = message.guild.get_role(int(first[0]))
                                    except ValueError:
                                        emb = Embed(title="══₪ TEAM LEAGUE ₪══",
                                                    description=f"**Ошибка в выборе команды. {mess[1]}**",
                                                    color=3553599)
                                        await message.channel.send(embed=emb)
                                        return
                                    if not checkRole:
                                        emb = Embed(title="══₪ TEAM LEAGUE ₪══",
                                                    description=f"**Ошибка в выборе команды. {mess[1]}**",
                                                    color=3553599)
                                        await message.channel.send(embed=emb)
                                        return

                                    second = re.search(r'\d+', mess[2])
                                    if not second:
                                        emb = Embed(title="══₪ TEAM LEAGUE ₪══",
                                                    description=f"**Ошибка в выборе команды. {mess[2]}**",
                                                    color=3553599)
                                        await message.channel.send(embed=emb)
                                        return
                                    try:
                                        checkRole = message.guild.get_role(int(second[0]))
                                    except ValueError:
                                        emb = Embed(title="══₪ TEAM LEAGUE ₪══",
                                                    description=f"**Ошибка в выборе команды. {mess[2]}**",
                                                    color=3553599)
                                        await message.channel.send(embed=emb)
                                        return

                                    if not checkRole:
                                        emb = Embed(title="══₪ TEAM LEAGUE ₪══",
                                                    description=f"**Ошибка в выборе команды. {mess[2]}**",
                                                    color=3553599)
                                        await message.channel.send(embed=emb)
                                        return
                                    del checkRole

                                    maps = await channels["map_pool"].fetch_message(860108051037290497)
                                    choose = choice(maps.content.split("\n"))

                                    emb = Embed(title="════₪ TEAM LEAGUE ₪════",
                                                description=f"**{mess[1]} vs {mess[2]}**\n"
                                                            f"**Ведущий: {message.author.mention}**\n"
                                                            f"**Карта: {choose}**",
                                                color=3553599)
                                    battleMessage = await message.channel.send(embed=emb)

                                    emb = Embed(title="════₪ TEAM LEAGUE ₪════",
                                                url=battleMessage.jump_url,
                                                description=f"**{mess[1]} vs {mess[2]}**\n"
                                                            f"**Ведущий: {message.author.mention}**\n"
                                                            f"**Карта: {choose}**\n"
                                                            f"**ID: `{battleMessage.id}`**",
                                                color=3553599)
                                    emb.set_footer(text="1️⃣ - победила первая команда\n"
                                                        "2️⃣ - победила вторая команда\n"
                                                        "⏹️- отмена матча""")
                                    del battleMessage, maps, choose, mess, message

                                    reactionMessage = await channels["match_logs"].send(embed=emb)
                                    await reactionMessage.add_reaction("1️⃣")
                                    await reactionMessage.add_reaction("2️⃣")
                                    await reactionMessage.add_reaction("⏹️")
                                    return

                                else:
                                    emb = Embed(title="══₪ TEAM LEAGUE ₪══",
                                                description=f"**Пользоваться `/battle` можно с 13:00 по 23:00 по мск.**",
                                                color=3553599)
                                    await message.channel.send(embed=emb)
                                    return

                if message.content.startswith("/addplayer") and message.channel == channels["payload"]:
                    startTime = time() + 3500 * 3
                    role = message.author.roles[1]

                    if str(role.color) != "#787d85":
                        await message.channel.send(embed=Embed(title="══₪ Добавление игроков ₪══",
                                                               description=f"У вас нет командной роли.",
                                                               color=3553599))
                        return

                    nickname = message.content.split()
                    if len(nickname) != 3:
                        await message.channel.send(embed=Embed(title="══₪ Добавление игроков ₪══",
                                                               description=f"Некорректный формат. `/addplayer (ник) (кто переводит)`",
                                                               color=3553599))
                        return

                    mess = await message.channel.send(embed=Embed(title="══₪ Добавление игроков ₪══",
                                                                  description=f"⏲️ Ожидание перевода от {nickname[-1]}. "
                                                                              f"На перевод дается 5 минут",
                                                                  color=3553599))

                    while startTime + 300 > time() + 3500 * 3:
                        payload = session.get("https://cp.vimeworld.ru/real?paylog")
                        soup = BeautifulSoup(payload.text, 'lxml')
                        transaction = soup.find_all("tr")
                        if not transaction:
                            await message.channel.send(embed=Embed(title="══₪ Добавление игроков ₪══",
                                                                   description=f"Личный кабинет упал. "
                                                                               f"Добавление игрока через транзакции невозможна",
                                                                   color=3553599))
                            return

                        transaction = transaction[1].text.split("\n")
                        transaction[2] = transaction[2].split()
                        del soup, payload

                        for i in range(len(month)):
                            if transaction[2][1] == month[i]:
                                transaction[2][1] = month_num[i]
                                break

                        if transaction[2][3][1] == ":":
                            transaction[2][3] = f"0{transaction[2][3]}"

                        transaction[2] = datetime.fromisoformat(
                            f"{transaction[2][2]}-{transaction[2][1]}-{transaction[2][0]} {transaction[2][3]}:00").timestamp()

                        if startTime < transaction[2]:
                            if transaction[3] == "+30" and nickname[-1] in transaction[-2]:
                                del transaction
                                userList = services["bot"].spreadsheets().values().get(spreadsheetId=sheet,
                                                                                       range=f'userlist!A2:B150',
                                                                                       majorDimension='ROWS'
                                                                                       ).execute()
                                if "values" not in userList:
                                    await mess.edit(embed=Embed(title="══₪ Добавление игроков ₪══",
                                                                description=f"UserListSheet: Возникла ошибка. Сообщите организаторам.",
                                                                color=3553599))

                                for num, team in enumerate(userList["values"]):
                                    if team[0].lower() == role.name.lower():
                                        del userList
                                        services["bot"].spreadsheets().values().batchUpdate(
                                            spreadsheetId=sheet,
                                            body={"valueInputOption": "USER_ENTERED",
                                                  "data": [{"range": f'userlist!B{num + 2}',
                                                            "majorDimension": "ROWS",
                                                            "values": [[f"{team[1]}, {nickname[2]}"]]}]}).execute()
                                        await mess.edit(embed=Embed(title="══₪ Добавление игроков ₪══",
                                                                    description=f"Игрок {nickname[2]} добавлен в команду {role.mention}",
                                                                    color=3553599))
                                        return
                        await sleep(5)

                    else:
                        await mess.edit(embed=Embed(title="══₪ Добавление игроков ₪══",
                                                    description=f"Время вышло.",
                                                    color=3553599))
                return

        async def on_raw_reaction_add(self, payload):
            if not payload.guild_id:
                return
            if payload.event_type != "REACTION_ADD":
                return
            if payload.channel_id != channels["match_logs"].id:
                return

            channel = self.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            del channel

            messageDescription = message.embeds[0].description.split("\n")
            roles = re.findall(r'\d+', messageDescription[0])
            if not roles:
                return
            author = re.search(r'\d+', messageDescription[1])
            if not author:
                return
            messageID = re.search(r'\d+', messageDescription[3])
            if not messageID:
                return
            del messageDescription

            if minecupRoles["org2"] in payload.member.roles or payload.member.id == int(author[0]):
                if str(payload.emoji) == "⏹️":
                    emb = Embed(title="════₪ TEAM LEAGUE ₪════",
                                url=f"https://discord.com/channels/856327254178791424/858273631033360384/{messageID[0]}",
                                description=f"**Отмена матча**\n"
                                            f"**Написал команду: <@{author[0]}>**\n"
                                            f"**Отменил матч: {payload.member.mention}**\n"
                                            f"**ID: `{messageID[0]}`**",
                                color=3553599)
                    await message.edit(embed=emb)
                    await message.clear_reactions()

                else:
                    guild = client.get_guild(856327254178791424)
                    roles[0] = guild.get_role(int(roles[0]))
                    roles[1] = guild.get_role(int(roles[1]))
                    del guild

                    length = 2
                    matches = services["bot"].spreadsheets().values().get(spreadsheetId=sheet,
                                                                          range=f'matches!A{str(length)}:B100',
                                                                          majorDimension='ROWS'
                                                                          ).execute()
                    if "values" in matches:
                        length += len(matches["values"])
                    del matches

                    if str(payload.emoji) == "1️⃣":
                        await infoToSheet(message, messageID[0], roles[0], roles[1], length, author,
                                          payload.member.mention)

                    elif str(payload.emoji) == "2️⃣":
                        await infoToSheet(message, messageID[0], roles[1], roles[0], length, author,
                                          payload.member.mention)

    client = MyClient()
    client.run(token["bot"])
