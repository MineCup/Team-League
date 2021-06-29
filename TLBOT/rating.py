from asyncio import sleep
from TLBOT.config import sheet


async def rating(services):
    try:
        getmatches = services["rating"].spreadsheets().values().get(spreadsheetId=sheet["team_league"],
                                                                    range=f'matches!A2:B1000',
                                                                    majorDimension='ROWS').execute()["values"]
        for i in range(0, len(getmatches)):
            teamrating = services["rating"].spreadsheets().values().get(spreadsheetId=sheet["team_league"],
                                                                        range=f'work!A2:D1000',
                                                                        majorDimension='ROWS').execute()["values"]
            services["rating"].spreadsheets().values().batchUpdate(spreadsheetId=sheet["team_league"],
                                                                   body={
                                                                       "valueInputOption": "USER_ENTERED",
                                                                       "data": [{"range": f'work!G7:H7',
                                                                                 "majorDimension": "ROWS",
                                                                                 "values": [[getmatches[i][0],
                                                                                             getmatches[i][1]]]}]}
                                                                   ).execute()

            getwork = services["rating"].spreadsheets().values().get(spreadsheetId=sheet["team_league"],
                                                                     range=f'work!G4:M4',
                                                                     majorDimension='COLUMNS').execute()["values"]
            team1 = 65536
            team2 = 65536
            for w in range(len(teamrating)):
                if teamrating[w][0].lower() == getmatches[i][0].lower():
                    team1 = w
                elif teamrating[w][0].lower() == getmatches[i][1].lower():
                    team2 = w
            print(f"Строка {i + 1}")
            print(team1, team2)
            if team1 != 65536 and team2 != 65536:
                if int(getwork[0][0]) - int(getwork[1][0]) >= 0:
                    print(">= 0")
                    services["rating"].spreadsheets().values().batchUpdate(spreadsheetId=sheet["team_league"],
                                                                           body={
                                                                               "valueInputOption": "USER_ENTERED",
                                                                               "data": [{
                                                                                   "range": f'work!A{team1 + 2}:D{team1 + 2}',
                                                                                   "majorDimension": "ROWS",
                                                                                   "values": [[teamrating[team1][0],
                                                                                               f"=E{team1 + 2}",
                                                                                               getwork[3][0],
                                                                                               int(teamrating[team1][
                                                                                                       3]) + 1]]}]}
                                                                           ).execute()
                    services["rating"].spreadsheets().values().batchUpdate(spreadsheetId=sheet["team_league"],
                                                                           body={
                                                                               "valueInputOption": "USER_ENTERED",
                                                                               "data": [{
                                                                                   "range": f'work!A{team2 + 2}:D{team2 + 2}',
                                                                                   "majorDimension": "ROWS",
                                                                                   "values": [[teamrating[team2][0],
                                                                                               f"=E{team2 + 2}",
                                                                                               getwork[6][0],
                                                                                               int(teamrating[team2][
                                                                                                       3]) + 1]]}]}
                                                                           ).execute()
                else:
                    print("< 0")
                    services["rating"].spreadsheets().values().batchUpdate(spreadsheetId=sheet["team_league"],
                                                                           body={
                                                                               "valueInputOption": "USER_ENTERED",
                                                                               "data": [{
                                                                                   "range": f'work!A{team1 + 2}:D{team1 + 2}',
                                                                                   "majorDimension": "ROWS",
                                                                                   "values": [[teamrating[team1][0],
                                                                                               f"=E{team1 + 2}",
                                                                                               getwork[4][0],
                                                                                               int(teamrating[team1][
                                                                                                       3]) + 1]]}]}
                                                                           ).execute()
                    services["rating"].spreadsheets().values().batchUpdate(spreadsheetId=sheet["team_league"],
                                                                           body={
                                                                               "valueInputOption": "USER_ENTERED",
                                                                               "data": [{
                                                                                   "range": f'work!A{team2 + 2}:D{team2 + 2}',
                                                                                   "majorDimension": "ROWS",
                                                                                   "values": [[teamrating[team2][0],
                                                                                               f"=E{team2 + 2}",
                                                                                               getwork[5][0],
                                                                                               int(teamrating[team2][
                                                                                                       3]) + 1]]}]}
                                                                           ).execute()
            else:
                print(f"Ошибка {team1}:{team2}")
            await sleep(2.3)
            getworkcheck = services["rating"].spreadsheets().values().get(spreadsheetId=sheet["team_league"],
                                                                          range=f'work!G4:M4',
                                                                          majorDimension='COLUMNS').execute()["values"]
            if getworkcheck == getwork:
                continue
        getmatches1 = services["rating"].spreadsheets().values().get(spreadsheetId=sheet["team_league"],
                                                           range=f'matches!A2:E4000',
                                                           majorDimension='COLUMNS').execute()["values"]
        getmatches2 = services["rating"].spreadsheets().values().get(spreadsheetId=sheet["team_league"],
                                                                     range=f'matches!G2:K4000',
                                                                     majorDimension='COLUMNS').execute()
        if "values" not in getmatches2:
            getmatches2 = [""]
        else:
            getmatches2 = getmatches2["values"]
        services["rating"].spreadsheets().values().batchUpdate(spreadsheetId=sheet["team_league"],
                                                               body={"valueInputOption": "USER_ENTERED",
                                                                     "data": [{
                                                                         "range": f'matches!G{len(getmatches2[0]) + 2}:K{len(getmatches2[0]) + 2 + len(getmatches1[0]) + 2}',
                                                                         "majorDimension": "COLUMNS",
                                                                         "values": [getmatches1[0],
                                                                                    getmatches1[1],
                                                                                    getmatches1[2],
                                                                                    getmatches1[3],
                                                                                    getmatches1[4]]}]}
                                                               ).execute()
        services["rating"].spreadsheets().values().batchUpdate(spreadsheetId=sheet["team_league"],
                                                               body={"valueInputOption": "USER_ENTERED",
                                                                     "data": [{
                                                                         "range": f'matches!A{2}:K{len(getmatches1[0]) + 2}',
                                                                         "majorDimension": "COLUMNS",
                                                                         "values": [[""] * len(getmatches1[1]),
                                                                                    [""] * len(getmatches1[1]),
                                                                                    [""] * len(getmatches1[1]),
                                                                                    [""] * len(getmatches1[1]),
                                                                                    [""] * len(getmatches1[1])]}]}
                                                               ).execute()
    except:
        print("Нет матчей.")
        await sleep(600)
    await sleep(10800)
