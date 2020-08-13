import random


class Player:
    def __init__(self, name):
        self.name = name
        self.elo = 2500
        self.previous_net_score = []
        self.win_streak = 0
        self.loose_streak = 0

    def __repr__(self):
        return "{name} -> {elo}".format(name=self.name, elo=self.elo)

    def __str__(self):
        return "{name} -> {elo}".format(name=self.name, elo=self.elo)


class Stats:
    def __init__(self):
        self.score = 0
        self.net_score = 0
        self.kill = 0
        self.death = 0
        self.assists = 0

    def __repr__(self):
        return "Score {score} net_score {net_score}".format(
            score=self.score, net_score=self.net_score
        )


class Elo:
    def __init__(self):
        self.K = 40
        self.weight_net_score = 5
        self.weight_assits = 2.2
        self.weight_consitency = 2.8
        self.weight_streak = 1.5

    def get_avg_elo(self, team):
        players = team["players"]
        return sum([player[0].elo for player in players]) / len(players)

    def compute_net_score(self, player, match):
        all_players = match.team1["players"] + match.team2["players"]
        all_net_score = [player[1].net_score for player in all_players]
        net_score = player[1].net_score
        net_score_align = 0
        if net_score > 0:
            net_score_align = net_score / max(max(all_net_score), 1)
        elif net_score < 0:
            net_score_align = net_score / max(abs(min(all_net_score)), 1)
        return self.weight_net_score * net_score_align

    def comput_assists(self, player, team):
        all_assits = [player[1].assists for player in team["players"]]
        number_assists_team = sum(all_assits)
        assists = player[1].assists

        max_all_assist_percent = max(all_assits) / max(number_assists_team, 1)
        assists_percent = assists / max(number_assists_team, 1)

        assit_allign = assists_percent / max_all_assist_percent

        return self.weight_assits * assit_allign

    def compute_consistency(self, player):
        if len(player[0].previous_net_score) >= 5:
            # Do thing here
            if len(player[0].previous_net_score) == 10:
                player[0].previous_net_score.pop(0)
            player[0].previous_net_score.append(player[1].net_score)
            return 0
        else:
            player[0].previous_net_score.append(player[1].net_score)
            return 0

    def compute_streak(self, player, hasWon):
        return 0

    def compute_elo(self, match):
        avg_elo_team1 = self.get_avg_elo(match.team1)
        avg_elo_team2 = self.get_avg_elo(match.team2)

        p1 = 1.0 / (1.0 + pow(10, ((avg_elo_team2 - avg_elo_team1) / 400.0)))
        p2 = 1.0 / (1.0 + pow(10, ((avg_elo_team1 - avg_elo_team2) / 400.0)))

        base_elo_team1 = 0
        base_elo_team2 = 0
        team1_won = False
        team2_won = False

        if match.team1["score"] > match.team2["score"]:
            team1_won = True
            base_elo_team1 = self.K * (1.0 - p1)
            base_elo_team2 = self.K * (0.0 - p2)
        elif match.team1["score"] < match.team2["score"]:
            team2_won = True
            base_elo_team1 = self.K * (0.0 - p1)
            base_elo_team2 = self.K * (1.0 - p2)
        else:
            return

        for player in match.team1["players"]:
            # Compute Indiv perf here
            indiv_elo = base_elo_team1
            indiv_elo += self.compute_net_score(player, match)
            indiv_elo += self.comput_assists(player, match.team1)
            indiv_elo += self.compute_consistency(player)
            indiv_elo += self.compute_streak(player, team1_won)
            player[0].elo += round(indiv_elo)

        for player in match.team2["players"]:
            # Compute Indiv perf here
            indiv_elo = base_elo_team2
            indiv_elo += self.compute_net_score(player, match)
            indiv_elo += self.comput_assists(player, match.team2)
            indiv_elo += self.compute_consistency(player)
            indiv_elo += self.compute_streak(player, team2_won)
            player[0].elo += round(indiv_elo)


class Match:
    def __init__(self, id):
        self.id = id
        self.team1 = {"score": 0, "players": []}
        self.team2 = {"score": 0, "players": []}

    def build_team(self):
        choices = random.sample(PLAYERS, k=12)
        for id in range(12):  # 12 player in the same match
            if id > 5:
                self.team2["players"].append([choices[id], Stats()])
            else:
                self.team1["players"].append([choices[id], Stats()])

    def run_match(self):
        nbOfAction = random.randint(150, 200)
        for _ in range(nbOfAction):
            condition = bool(random.getrandbits(1))
            team_attack = self.team1
            team_target = self.team2
            attacker_selected = random.randint(1, 3)
            if condition:
                team_attack = self.team2
                team_target = self.team1
            attackers = random.sample(team_attack["players"], k=attacker_selected)
            target = random.choice(team_target["players"])
            team_attack["score"] += 1
            attackers[0][1].score += 1
            attackers[0][1].net_score += 1
            target[1].net_score -= 1
            attackers[0][1].kill += 1
            target[1].death += 1
            if bool(random.getrandbits(1)):  # 50% change of kill being an assist
                for i in range(1, attacker_selected):
                    attackers[i][1].assists += 1


def run_simulation(ELO):
    for id in range(50):
        match = Match(id)
        match.build_team()
        match.run_match()
        ELO.compute_elo(match)
        MATCHES.append(match)


MATCHES = []
PLAYERS = [Player(i) for i in range(1, 16)]


def main():
    ELO = Elo()
    run_simulation(ELO)


if __name__ == "__main__":
    main()
