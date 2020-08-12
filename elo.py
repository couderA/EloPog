import random


class Player:
    def __init__(self, name):
        self.name = name
        self.elo = 2500
        self.previousNetScore = []
        self.winStreak = 0
        self.looseStreak = 0

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


class Stats:
    def __init__(self):
        self.score = 0
        self.netScore = 0
        self.kill = 0
        self.death = 0

    def __repr__(self):
        return "Score {score} NetScore {netScore}".format(
            score=self.score, netScore=self.netScore
        )


class Elo:
    def __init__(self):
        self.K = 40
        self.WeightNetScore = 5
        self.WeightAsssits = 0
        self.WeightConsitency = 3
        self.WeightStreak = 3

    def getAvgElo(self, team):
        players = team["players"]
        return sum([player[0].elo for player in players]) / len(players)

    def computeNetScore(self, player, match):
        return 0

    def computAssists(self, player, team):
        return 0

    def computeConsistency(self, player):
        if len(player[0].previousNetScore) >= 5:
            # Do thing here
            if len(player[0].previousNetScore) == 10:
                player[0].previousNetScore.pop(0)
            player[0].previousNetScore.append(player[1].netScore)
            return 0
        else:
            player[0].previousNetScore.append(player[1].netScore)
            return 0

    def computeStreak(self, player, hasWon):
        return 0

    def computeElo(self, match):
        AvgEloTeam1 = self.getAvgElo(match.team1)
        AvgEloTeam2 = self.getAvgElo(match.team2)

        print(match.team1)
        print(match.team2)

        p1 = 1.0 / (1.0 + pow(10, ((AvgEloTeam2 - AvgEloTeam1) / 400.0)))
        p2 = 1.0 / (1.0 + pow(10, ((AvgEloTeam1 - AvgEloTeam2) / 400.0)))

        baseEloTeam1 = 0
        baseEloTeam2 = 0
        team1Won = False
        team2Won = False

        if match.team1["score"] > match.team2["score"]:
            team1Won = True
            baseEloTeam1 = round(self.K * (1.0 - p1))
            baseEloTeam2 = round(self.K * (0.0 - p2))
        elif match.team1["score"] < match.team2["score"]:
            team2Won = True
            baseEloTeam1 = round(self.K * (0.0 - p1))
            baseEloTeam2 = round(self.K * (1.0 - p2))
        else:
            return

        print(baseEloTeam1)
        print(baseEloTeam2)

        for player in match.team1["players"]:
            # Compute Indiv perf here
            indivElo = baseEloTeam1
            indivElo += computeNetScore(player, match)
            indivElo += computAssists(player, match.team1)
            indivElo += computeConsistency(player)
            indivElo += computeStreak(player, team1Won)
            player[0].elo += indivElo

        for player in match.team2["players"]:
            # Compute Indiv perf here
            indivElo = baseEloTeam2
            indivElo += computeNetScore(player, match)
            indivElo += computAssists(player, match.team)
            indivElo += computeConsistency(player)
            indivElo += computeStreak(player, team2Won)
            player[0].elo += baseEloTeam2


class Match:
    def __init__(self, id):
        self.id = id
        self.team1 = {"score": 0, "players": []}
        self.team2 = {"score": 0, "players": []}

    def buildTeam(self):
        choices = random.sample(players, k=12)
        for id in range(12):  # 12 player in the same match
            if id > 5:
                self.team2["players"].append([choices[id], Stats()])
            else:
                self.team1["players"].append([choices[id], Stats()])

    def runMatch(self):
        nbOfAction = random.randint(150, 200)
        for _ in range(nbOfAction):
            condition = bool(random.getrandbits(1))
            teamAttack = self.team1
            teamTarget = self.team2
            if condition:
                teamAttack = self.team2
                teamTarget = self.team1
            attacker = random.choice(teamAttack["players"])
            target = random.choice(teamTarget["players"])
            teamAttack["score"] += 1
            attacker[1].score += 1
            attacker[1].netScore += 1
            target[1].netScore -= 1
            attacker[1].kill += 1
            target[1].death += 1


matches = []


def runSimulation():
    for id in range(1):
        print("Match {0}".format(id))
        match = Match(id)
        match.buildTeam()
        match.runMatch()
        ELO.computeElo(match)
        matches.append(match)
        print("")
    print(players)


ELO = Elo()
runSimulation()
