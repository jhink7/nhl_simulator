import numpy as np
import pandas as pd
from game_simulator import GameSimulator
from series_simulator import SeriesSimulator
from team import Team

class PlayoffSimulator(object):
    game_simulator = GameSimulator()
    series_simulator = SeriesSimulator(game_simulator)

    # simulate conference
    def sim_conference(self, seed1, seed2, seed3, seed4, seed5, seed6, seed7, seed8):
        # round 1
        r1_w1 = self.series_simulator.simulate_series(seed1, seed8)
        r1_w2 = self.series_simulator.simulate_series(seed2, seed7)
        r1_w3 = self.series_simulator.simulate_series(seed3, seed6)
        r1_w4 = self.series_simulator.simulate_series(seed4, seed5)

        # round 2
        r2_w1 = self.series_simulator.simulate_series(r1_w1, r1_w4)
        r2_w2 = self.series_simulator.simulate_series(r1_w2, r1_w3)

        # round 3 (conference finals)
        conf_champ = self.series_simulator.simulate_series(r2_w1, r2_w2)

        return conf_champ


    def sim_playoffs(self, east_teams, west_teams):
        # simulate conferences
        east_champ = self.sim_conference(east_teams[0], 
                                         east_teams[1], 
                                         east_teams[2], 
                                         east_teams[3], 
                                         east_teams[4], 
                                         east_teams[5], 
                                         east_teams[6], 
                                         east_teams[7])
        west_champ = self.sim_conference(west_teams[0],
                                         west_teams[1], 
                                         west_teams[2], 
                                         west_teams[3], 
                                         west_teams[4], 
                                         west_teams[5], 
                                         west_teams[6], 
                                         west_teams[7])

        # simulate stanley cup final

        # for simulation purposes, determine home ice with a coin flip
        flip = np.random.uniform(0,1,1)

        if(flip[0] < 0.5):
            champ = self.series_simulator.simulate_series(east_champ, west_champ)
        else:
            champ = self.series_simulator.simulate_series(west_champ, east_champ)

        return champ


