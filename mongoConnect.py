from pymongo import MongoClient
from collections import defaultdict
cluster = "mongodb+srv://grovetender:562010RfACQbYAQi@faygrove.c0zaa.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(cluster)

class Highscores():
    def __init__(self):
        highscores = client["HighscoresForOpSnowflake"]
        self.highs = highscores.Highscores
        self.col = highscores["Highscores"]

    def insertHighscore(self, name, score):
        if not self.col.find_one({"name": name}):
            self.col.insert_one({"name": name.lower(), "scores": [score]})
        else:
            self.col.update_one({"name": name}, { "$addToSet": { "scores": score}})

    def getFiveHighestScores(self):
        #Dict max values, sorted/sort
        #Sort dict take the five largest keys or values to list and use that to display the best scores
        highestDict = {}
        sortedDict = {}
        for score in self.col.find():
            highestDict.update({score["name"]: max(score["scores"])})
        tList = sorted(highestDict.items(), key = lambda item: item[1], reverse=True)
        for key, value in tList:
            sortedDict[key] = value
        return sortedDict

    def getUserHighestScores(self, name):
        highestDict = defaultdict(list)
        sortedDict = {}
        for item in self.col.find_one({"name": name})["scores"]:
            highestDict[name].append(item)
        tList = sorted(highestDict[name], reverse=True)
        sortedDict.update({name: tList})
        return sortedDict

high = Highscores()
high.getUserHighestScores('joona')