# EloPog
Elo Algorithm for the POG Discord Bot based on a Custom Chess Elo Algorithm


## To Do List
### Compute Base Elo
- [x] Classic Chess Elo between the average elo of each Team.

### Compute Individual Elo from direct Perf on the match
- [x] Compute Individual Elo on the netScore compare to everyone in the match
- [x] Compute Individual Elo on the number of assist compare to everyone in player's team

### Compute Individual Elo from direct Perf comparing his past
- [ ] Compute Individual Elo base on Consistency on the 10 previous match
- [ ] Compute Individual Elo based on the Winning/Losing Streak

## Algo Explain
Starting Elo at **2500** middle point to 0 and 5000 which is the Min and Max.

Everyone in the same team win or loose the same base amount of Elo.

The NetScore part of the individual Elo reward the best player of the game and punish the worst
The Assits part of the individual Elo reward depending on the assists contribution for his team

The Consistency part of the individual Elo reward the player when he plays better than his past Average netScore
The Streak part of the individual Elo reward for having a Win streak and punish for having a loose streak

At the end of each match,  

## Data Example:
![Data](https://cdn.discordapp.com/attachments/724265953445019678/731919056508026890/unknown.png)
Some data are missing here like assists and TK that could be used
