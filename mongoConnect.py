from pymongo import MongoClient
#xcYHWeCKD7XixvK
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
        first = 0
        second = 0
        third = 0
        fourth = 0
        fifth = 0