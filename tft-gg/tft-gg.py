import requests
from prettytable import PrettyTable
import sys, threading, time

def animation():
    for char in ['|', '/', '-', '\\']:
        sys.stdout.write('\r' + char)
        time.sleep(0.1)
        sys.stdout.flush()

def checkName(name):
    summonerName = "https://na1.api.riotgames.com/tft/summoner/v1/summoners/by-name/" + name
    
    r = requests.get(summonerName, headers={"X-Riot-Token": "RGAPI-8fc7bd06-ba30-49aa-acc7-ba3f88769a8d"})

    if (r.status_code == 200):
        print("name checks out!")
        return(True)
    else:
        print("invalid name!\n")
        return(False)


# function that takes a player's PUUID and returns their in-game name
def getName(puuid):
    summonerName = "https://na1.api.riotgames.com/tft/summoner/v1/summoners/by-puuid/" + puuid

    r = requests.get(summonerName, headers={"X-Riot-Token": "RGAPI-8fc7bd06-ba30-49aa-acc7-ba3f88769a8d"})

    jsonDictionary = r.json()
    name = jsonDictionary["name"]

    return name

# function that takes a player's in-game name and returns their PUUID
def getPUUID(name):
    summonerName = "https://na1.api.riotgames.com/tft/summoner/v1/summoners/by-name/" + name

    r = requests.get(summonerName, headers={"X-Riot-Token": "RGAPI-8fc7bd06-ba30-49aa-acc7-ba3f88769a8d"})

    jsonDictionary = r.json()
    puuid = jsonDictionary["puuid"]

    return puuid

# function that takes a player's in-game name and returns their ID
def getID(name):
    summonerName = "https://na1.api.riotgames.com/tft/summoner/v1/summoners/by-name/" + name

    r = requests.get(summonerName, headers={"X-Riot-Token": "RGAPI-8fc7bd06-ba30-49aa-acc7-ba3f88769a8d"})

    jsonDictionary = r.json()
    id = jsonDictionary["id"] 

    return id

def getTier(id):
    encryptedID = "https://na1.api.riotgames.com/tft/league/v1/entries/by-summoner/" + id

    r = requests.get(encryptedID, headers={"X-Riot-Token": "RGAPI-8fc7bd06-ba30-49aa-acc7-ba3f88769a8d"})

    jsonDictionary = r.json()

    for d in jsonDictionary:
        tier = d["tier"]

    return tier

def getRank(id):
    encryptedID = "https://na1.api.riotgames.com/tft/league/v1/entries/by-summoner/" + id

    r = requests.get(encryptedID, headers={"X-Riot-Token": "RGAPI-8fc7bd06-ba30-49aa-acc7-ba3f88769a8d"})

    jsonDictionary = r.json()

    for d in jsonDictionary:
        rank = d["rank"]

    return rank

# function that takes a player's ID and returns their Tier and Rank
def getRankAndTier(id):
    encryptedID = "https://na1.api.riotgames.com/tft/league/v1/entries/by-summoner/" + id

    r = requests.get(encryptedID, headers={"X-Riot-Token": "RGAPI-8fc7bd06-ba30-49aa-acc7-ba3f88769a8d"})

    jsonDictionary = r.json()

    for d in jsonDictionary:
        tier = d["tier"]
        rank = d["rank"]

    return tier + " " + rank

# function that takes a player's ID and returns the amount of League Points they have
def getLP(id):
    encryptedID = "https://na1.api.riotgames.com/tft/league/v1/entries/by-summoner/" + id

    r = requests.get(encryptedID, headers={"X-Riot-Token": "RGAPI-8fc7bd06-ba30-49aa-acc7-ba3f88769a8d"})

    jsonDictionary = r.json()

    for d in jsonDictionary:
        lp = d["leaguePoints"] 

    return lp

# function that takes a player's ID and returns their win rate in Ranked
def getWinrate(id):
    encryptedID = "https://na1.api.riotgames.com/tft/league/v1/entries/by-summoner/" + id

    r = requests.get(encryptedID, headers={"X-Riot-Token": "RGAPI-8fc7bd06-ba30-49aa-acc7-ba3f88769a8d"})

    jsonDictionary = r.json()

    for d in jsonDictionary:
        wins = d["wins"]
        total = wins + d["losses"]

    return str(round(wins/total * 100, 2)) + "%"

# function that takes a player's PUUID and returns a list of their 3 most recent matches
def getMatchID(puuid):
    matchHistory = "https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/" + puuid + "/ids?count=3"

    r = requests.get(matchHistory, headers={"X-Riot-Token": "RGAPI-8fc7bd06-ba30-49aa-acc7-ba3f88769a8d"})

    jsonDictionary = r.json()
    matches = jsonDictionary
    
    return matches

# function that takes a matches ID and returns info about that game in the format of a JSON dictionary
def getMatchInfo(matchid):
    matchInfo = "https://americas.api.riotgames.com/tft/match/v1/matches/" + matchid

    r = requests.get(matchInfo, headers={"X-Riot-Token": "RGAPI-8fc7bd06-ba30-49aa-acc7-ba3f88769a8d"})

    jsonDictionary = r.json()
    
    return jsonDictionary

# function that takes a JSON dictionary of a match's information and returns a list of the players' names who were in the game
# returned list is in order of placement (1st to 8th)
def getPlayers(dictionary):
    participants = dictionary["info"]["participants"]

    participantNames = [0, 1, 2, 3, 4, 5, 6, 7]

    for x in range(0, 8):
        currentParticipant = participants[x]
        participantNames[currentParticipant["placement"] - 1] = getName(currentParticipant["puuid"])

    return participantNames

# function that takes a JSON dictionary of a match's information and returns a list of the players' levels who were in the game
# returned list is in order of placement(1st to 8th)
def getLevels(dictionary):
    participants = dictionary["info"]["participants"]

    participantLevels = [0, 1, 2, 3, 4, 5, 6, 7]

    for x in range(0, 8):
        currentParticipant = participants[x]
        participantLevels[currentParticipant["placement"] - 1] = currentParticipant["level"]

    return participantLevels

def getRound(dictionary):
    participants = dictionary["info"]["participants"]

    participantRound = [0, 1, 2, 3, 4, 5, 6, 7]

    for x in range(0, 8):
        currentParticipant = participants[x]
        participantRound[currentParticipant["placement"] - 1] = currentParticipant["last_round"]

    return participantRound

def getTime(dictionary):
    participants = dictionary["info"]["participants"]

    participantTime = [0, 1, 2, 3, 4, 5, 6, 7]

    for x in range(0, 8):
        currentParticipant = participants[x]
        participantTime[currentParticipant["placement"] - 1] = round(currentParticipant["time_eliminated"]/60, 2)

    return participantTime

def getPlayerInfo(name):
    # get relevant info and assign them to variables
    id = getID(name)
    rank = getRankAndTier(id)
    lp = getLP(id)
    winrate = getWinrate(id)

    # create table of requested player's info
    playerInfo = PrettyTable()
    playerInfo.title = "Player " + name + "'s Profile"
    playerInfo.field_names = ["Rank", "League Points", "Win Rate"]
    playerInfo.add_row([rank, lp, winrate])
    
    return playerInfo

def getMatchDetails(name):
    # get relevant info and assign them to variables
    puuid = getPUUID(name)
    matches = getMatchID(puuid)
 
    matchinfo = getMatchInfo(matches[0])

    # create table of requested player's most recent match details
    matchDetails = PrettyTable()
    matchDetails.title = "Most Recent Match Details"
    column_names = ["Players", "Levels", "Last Round", "Alive"]
    matchDetails.add_column(column_names[0], getPlayers(matchinfo))
    matchDetails.add_column(column_names[1], getLevels(matchinfo))
    matchDetails.add_column(column_names[2], getRound(matchinfo))
    matchDetails.add_column(column_names[3], getTime(matchinfo))
    
    return matchDetails

# function that takes a name and displays the requested player's info and details of their most recent match
def displayAllInfo(name):
    # display player info table
    print(getPlayerInfo(name))
    # display match details table
    print(getMatchDetails(name))

# takes the name of two players and determines who is more likely to win based off their ranks
def comparePlayers(name1, name2):
    tierDict = {"IRON" : 0,
                "BRONZE" : 1,
                "SILVER" : 2,
                "GOLD" : 3,
                "PLATINUM" : 4,
                "DIAMOND" : 5,
                "MASTER" : 6,
                "GRANDMASTER" : 7,
                "CHALLENGER" : 8
    }

    rankDict = {"I" : 1,
                "II" : 2,
                "III" : 3,
                "IV" : 4,
                "V" : 5
    }

    id1 = getID(name1)
    id2 = getID(name2)

    tier1 = tierDict.get(getTier(id1))
    tier2 = tierDict.get(getTier(id2))

    rank1 = rankDict.get(getRank(id1))
    rank2 = rankDict.get(getRank(id2))

    if (tier1 > tier2):
        return name1
    elif (tier1 == tier2):
        if (rank1 > rank2):
            return name1
        else:
            return name2
    else:
        return name2

# function that displays the winner based on the comparePlayers function's results
def displayWinner(name1, name2):
    print(comparePlayers(name1, name2) + " is more likely to win")

# application 
while (True):
    print("Type 'compare' to see who is more likely to win\nType 'search' to see a player's profile\nType 'quit' to end application")
    command = input("input: ")

    if (command.lower().replace(" ", "") == "search"):
        name = input("\nWhat is the summoner name you want to look up?: ").replace(" ", "").lower()

        if (checkName(name) == True):
            theProcess = threading.Thread(name='process', target=displayAllInfo, args=(name,))
            theProcess.start()
            while (theProcess.isAlive()):
                animation() 
            print("\n")
    
    elif (command.lower().replace(" ", "") == "compare"):
        name1 = input("\nType the name of the first player: ")

        if (checkName(name1) == True):
            name2 = input("Type the name of the second player: ")
            if (checkName(name2) == True):
                theProcess = threading.Thread(name='process', target=displayWinner, args=(name1, name2,))
                theProcess.start()
                while (theProcess.isAlive()):
                    animation()
                print("\n")

    elif (command.lower().replace(" ", "") == "quit"):
        exit()

    else:
        print("invalid input")

