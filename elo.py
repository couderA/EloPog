import random

class Player():
    def __init__(self, name):
        self.name = name
        self.elo = 2500

    def __repr__(self):
        return "{name} -> {elo}".format(name=self.name, elo=self.elo)

    def __str__(self):
        return "{name} -> {elo}".format(name=self.name, elo=self.elo)

players = [
    Player("1"),
    Player("2"),
    Player("3"),
    Player("4"),
    Player("5"),
    Player("6"),
    Player("7"),
    Player("8"),
    Player("9"),
    Player("10"),
    Player("11"),
    Player("12"),
    Player("13"),
    Player("14"),
    Player("15"),
]


for player in players:
    print(player)

class Stats():
    def __init__(self):
        self.score = 0
        self.netScore = 0
        self.kill = 0
        self.death = 0

class Match():
    def __init__(self, id):
        self.id = id
        self.team1 = []
        self.team2 = []

    def buildTeam(self):
        choices = random.sample(players, k=12)
        for id in range(0, 12): # 12 player in the same match
            if id > 5:
                self.team2.append([choices[id], Stats()])
            else:
                self.team1.append([choices[id], Stats()])


matches = []

for id in range(1, 3):
    print("Match {0}".format(id))
    match = Match(id)
    match.buildTeam()
    print("Team 1")
    print(match.team1)
    print("Team 2")
    print(match.team2)
    # match.computeEloForPlayer()
    matches.append(match)
    print("")