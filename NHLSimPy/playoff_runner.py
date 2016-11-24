import numpy as np
import pandas as pd
from game_simulator import GameSimulator
from series_simulator import SeriesSimulator
from playoff_simulator import PlayoffSimulator
from team import Team

# instantiate our core game simulator
game_simulator = GameSimulator()
series_simulator = SeriesSimulator(game_simulator)

east1 = Team('East1', 3.5, 2.7)
east2 = Team('East2', 3.4, 2.8)
east3 = Team('East3', 3.4, 3.0)
east4 = Team('East4', 3.3, 3.0)
east5 = Team('East5', 3.3, 3.1)
east6 = Team('East6', 3.2, 3.0)
east7 = Team('East7', 3.2, 3.1)
east8 = Team('East8', 3.1, 3.1)

west1 = Team('West1', 3.5, 2.7)
west2 = Team('West2', 3.4, 2.8)
west3 = Team('West3', 3.4, 3.0)
west4 = Team('West4', 3.3, 3.0)
west5 = Team('West5', 3.3, 3.1)
west6 = Team('West6', 3.2, 3.0)
west7 = Team('West7', 3.2, 3.1)
west8 = Team('West8', 3.1, 3.1)

east_teams = [east1, east2, east3, east4, east5, east6, east7, east8]
west_teams = [west1, west2, west3, west4, west5, west6, west7, west8]
teams = east_teams + west_teams

playoff_sim = PlayoffSimulator();
champs = []

num_runs = 100

for i in range(0, num_runs):
    champ = playoff_sim.sim_playoffs(east_teams, west_teams)
    champs.append(champ)

# summarize sample run
champ_probs = []
for team in teams:
    #print team.name + ' ' + str(len([champ for champ in champs if champ.name == team.name]) / 100.0)
    champ_probs.append(len([champ for champ in champs if champ.name == team.name]) / float(num_runs))

results = pd.DataFrame({'team':[team.name for team in teams], 'champ_prob': champ_probs})
print results