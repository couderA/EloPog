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


class Stats:
    def __init__(self):
        self.score = 0
        self.netScore = 0
        self.kill = 0
        self.death = 0
        self.assists = 0

    def __repr__(self):
        return "Score {score} NetScore {netScore}".format(
            score=self.score, netScore=self.netScore
        )


class Elo:
    def __init__(self):
        self.K = 40
        self.weightNetScore = 5
        self.weightAsssits = 2.2
        self.weightConsitency = 2.8
        self.weightStreak = 1.5

    def getAvgElo(self, team):
        players = team["players"]
        return sum([player[0].elo for player in players]) / len(players)

    def computeNetScore(self, player, match):
        allPlayers = match.team1["players"] + match.team2["players"]
        allNetScore = [player[1].netScore for player in allPlayers]
        netscore = player[1].netScore
        netScoreAlign = 0
        if netscore > 0:
            netScoreAlign = netscore / max(max(allNetScore), 1)
        elif netscore < 0:
            netScoreAlign = netscore / max(abs(min(allNetScore)), 1)
        return self.weightNetScore * netScoreAlign

    def computAssists(self, player, team):
        allAsssits = [player[1].assists for player in team["players"]]
        numberAssistsTeam = sum(allAsssits)
        assists = player[1].assists

        maxAllAssistPercent = max(allAsssits) / max(numberAssistsTeam, 1)
        assistsPercent = assists / max(numberAssistsTeam, 1)

        asssitAllign = assistsPercent / maxAllAssistPercent

        return self.weightAsssits * asssitAllign

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

        p1 = 1.0 / (1.0 + pow(10, ((AvgEloTeam2 - AvgEloTeam1) / 400.0)))
        p2 = 1.0 / (1.0 + pow(10, ((AvgEloTeam1 - AvgEloTeam2) / 400.0)))

        baseEloTeam1 = 0
        baseEloTeam2 = 0
        team1Won = False
        team2Won = False

        if match.team1["score"] > match.team2["score"]:
            team1Won = True
            baseEloTeam1 = self.K * (1.0 - p1)
            baseEloTeam2 = self.K * (0.0 - p2)
        elif match.team1["score"] < match.team2["score"]:
            team2Won = True
            baseEloTeam1 = self.K * (0.0 - p1)
            baseEloTeam2 = self.K * (1.0 - p2)
        else:
            return

        for player in match.team1["players"]:
            # Compute Indiv perf here
            indivElo = baseEloTeam1
            indivElo += self.computeNetScore(player, match)
            indivElo += self.computAssists(player, match.team1)
            indivElo += self.computeConsistency(player)
            indivElo += self.computeStreak(player, team1Won)
            player[0].elo += round(indivElo)

        for player in match.team2["players"]:
            # Compute Indiv perf here
            indivElo = baseEloTeam2
            indivElo += self.computeNetScore(player, match)
            indivElo += self.computAssists(player, match.team2)
            indivElo += self.computeConsistency(player)
            indivElo += self.computeStreak(player, team2Won)
            player[0].elo += round(indivElo)


class Match:
    def __init__(self, id):
        self.id = id
        self.team1 = {"score": 0, "players": []}
        self.team2 = {"score": 0, "players": []}

    def buildTeam(self):
        choices = random.sample(PLAYERS, k=12)
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
            attackerSelected = random.randint(1, 3)
            if condition:
                teamAttack = self.team2
                teamTarget = self.team1
            attackers = random.sample(teamAttack["players"], k=attackerSelected)
            target = random.choice(teamTarget["players"])
            teamAttack["score"] += 1
            attackers[0][1].score += 1
            attackers[0][1].netScore += 1
            target[1].netScore -= 1
            attackers[0][1].kill += 1
            target[1].death += 1
            if bool(random.getrandbits(1)):  # 50% change of kill being an assist
                for i in range(1, attackerSelected):
                    attackers[i][1].assists += 1


def runSimulation(ELO):
    for id in range(100):
        match = Match(id)
        match.buildTeam()
        match.runMatch()
        ELO.computeElo(match)
        MATCHES.append(match)


MATCHES = []
PLAYERS = [Player(i) for i in range(1, 16)]


def main():
    ELO = Elo()
    runSimulation(ELO)


if __name__ == "__main__":
    main()
