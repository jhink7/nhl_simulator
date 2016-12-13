import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')

from game_simulator import GameSimulator

# instantiate our core game simulator
game_simulator = GameSimulator()

# setup lists used for analysis of results
all_home_goals = []
all_away_goals = []
all_home_wins = []
all_away_wins = []
all_home_OTLs = []
all_away_OTLs = []
all_home_SOLs = []
all_away_SOLs = []

for x in range(0, 10000):
    home_goals, away_goals, home_wins, away_wins, home_OTLs, away_OTLs, home_SOLs, away_SOLs, event_chart = game_simulator.simulate_game_poisson(3,3, 3, 3, False, False, False)
    all_home_goals.append(home_goals)
    all_away_goals.append(away_goals)
    all_home_wins.append(home_wins)
    all_away_wins.append(away_wins)
    all_home_OTLs.append(home_OTLs)
    all_away_OTLs.append(away_OTLs)
    all_home_SOLs.append(home_SOLs)
    all_away_SOLs.append(away_SOLs)

df = pd.DataFrame({'awayG': all_away_goals, 'homeG': all_home_goals, 
                   'homeW': all_home_wins, 'awayW': all_away_wins, 
                   'homeOTL': all_home_OTLs, 'awayOTL': all_away_OTLs, 
                   'homeSOL': all_home_SOLs, 'awaySOL': all_away_SOLs})

df['homeP'] = df.homeW * 2 + df.homeOTL + df.homeSOL
df['awayP'] = df.awayW * 2 + df.awayOTL + df.awaySOL

print df['homeG'].mean()
print df['awayG'].mean()

#print df['homeP'].mean()
#print df['awayP'].mean()

# histogram of simmed goals

plt.hist(df['homeG'], normed=False, color='b', label='Home Goals')
plt.hist(df['awayG'], normed=False, color='r', alpha=0.5, label='Away Goals')
plt.title("Goals Scored")
plt.xlabel("Value")
plt.ylabel("Probability")
plt.legend()
plt.show()

# histogram of simmed points
#plt.clf()
#plt.hist(df['homeP'], color='b', label='Home Points')
#plt.hist(df['awayP'], color='r', alpha=0.5, label='Away Points')
#plt.title("Points")
#plt.xlabel("Value")
#plt.ylabel("Probability")
#plt.legend()
#plt.xlim(0, 2.5)
#plt.show()

# demonstrate running goal chart
#home_goals, away_goals, home_wins, away_wins, home_OTLs, away_OTLs, home_SOLs, away_SOLs, event_chart = game_simulator.simulate_game_poisson(3.25,3.25, 3, 3, False, False, False)
#plt.plot(list(event_chart['iat']), list(event_chart['homeG']), 'r', list(event_chart['iat']), list(event_chart['awayG']), 'b')
#plt.ylabel("Goals")
#plt.xlabel("Event Time")
#plt.ylim(0,max(home_goals, away_goals) + 1)
#plt.title("Running Goals (Home in Red)")
#plt.legend()
#plt.show()