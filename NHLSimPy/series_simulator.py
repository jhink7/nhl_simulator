class SeriesSimulator(object):
    """An NHL Playoff Series Simulator"""

    def __init__(self, game_simulator):
        self.game_simulator = game_simulator

    def simulate_series(self, high_seed, low_seed):
        high_seed_wins = 0
        low_seed_wins = 0

        # games 1 & 2 (high seed at home)
        for i in range(0,2):
            home_wins, away_wins = self.simulate_series_game(high_seed, low_seed)
            high_seed_wins += home_wins
            low_seed_wins += away_wins

        # game 3 and 4 (low seed at home)
        for i in range(0,2):
            home_wins, away_wins = self.simulate_series_game(low_seed, high_seed)
            high_seed_wins += away_wins
            low_seed_wins += home_wins

        # game 5 (high seed at home)
        if high_seed_wins < 4 and low_seed_wins < 4:
            home_wins, away_wins = self.simulate_series_game(high_seed, low_seed)
            high_seed_wins += home_wins
            low_seed_wins += away_wins

        # game 6 (low seed at home)
        if high_seed_wins < 4 and low_seed_wins < 4:
            home_wins, away_wins = self.simulate_series_game(low_seed, high_seed)
            high_seed_wins += away_wins
            low_seed_wins += home_wins

        # game 7 (high seed at home)
        if high_seed_wins < 4 and low_seed_wins < 4:
            home_wins, away_wins = self.simulate_series_game(high_seed, low_seed)
            high_seed_wins += home_wins
            low_seed_wins += away_wins

        if high_seed_wins > low_seed_wins:
            return high_seed
        else:
            return low_seed

    def simulate_series_game(self, home_team, away_team):
        home_goals, away_goals, home_wins, away_wins, home_OTLs, away_OTLs, home_SOLs, away_SOLs, event_chart = self.game_simulator.simulate_game_poisson(home_team.gf, home_team.ga, away_team.gf, away_team.ga, False, False, True)
        return home_wins, away_wins

