import numpy as np
import pandas as pd

class GameSimulator:
    GOAL_SD = 1.583 #tweakable
    OT_TIE_THRESH = 3.85
    REG_TIE_THRESH = 0.5
    HOME_ICE_AD = 0.040

    def simulate_game(self, home_gf_neut, home_ga_neut, away_gf_neut, away_ga_neut, home_b2b, away_b2b, is_playoffs):
        home_sched_boost = 0
        
        if home_b2b and away_b2b:
            home_sched_boost = 0.014
        elif not home_b2b and not away_b2b:
            home_sched_boost = 0
        elif home_b2b and not away_b2b:
            home_sched_boost = -0.012
        else:
            home_sched_boost = 0.03

        home_gf = np.random.normal(home_gf_neut, self.GOAL_SD, 1) * (1 + home_sched_boost + self.HOME_ICE_AD)
        home_ga = np.random.normal(home_ga_neut, self.GOAL_SD, 1) / (1 + home_sched_boost + self.HOME_ICE_AD)

        away_gf = np.random.normal(away_gf_neut, self.GOAL_SD, 1) / (1 + home_sched_boost + self.HOME_ICE_AD)
        away_ga = np.random.normal(away_ga_neut, self.GOAL_SD, 1) * (1 + home_sched_boost + self.HOME_ICE_AD)

        home_goals = (home_gf + away_ga) / 2.0
        away_goals = (home_ga + away_gf) / 2.0

        home_wins = 0
        away_wins = 0
        home_OTLs = 0
        away_OTLs = 0
        home_SOLs = 0
        away_SOLs = 0

        if not is_playoffs:
            if abs(home_goals - away_goals) > self.REG_TIE_THRESH:
                if home_goals > away_goals:
                    home_wins = 1
                else:
                    away_wins = 1
            else:
                # game goes to OT
                home_gf_ot = np.random.normal(home_gf_neut, self.GOAL_SD * 3.0, 1) * (1 + home_sched_boost + self.HOME_ICE_AD)
                home_ga_ot = np.random.normal(home_ga_neut, self.GOAL_SD * 3.0, 1) / (1 + home_sched_boost + self.HOME_ICE_AD)

                away_gf_ot = np.random.normal(away_gf_neut, self.GOAL_SD * 3.0, 1) / (1 + home_sched_boost + self.HOME_ICE_AD)
                away_ga_ot = np.random.normal(away_ga_neut, self.GOAL_SD * 3.0, 1) * (1 + home_sched_boost + self.HOME_ICE_AD)

                home_goals_ot = (home_gf_ot + away_ga_ot) / 2.0
                away_goals_ot = (home_ga_ot + away_gf_ot) / 2.0

                ot_diff = home_goals_ot - away_goals_ot

                if ot_diff > 1:
                    home_wins = 1
                    away_OTLs = 1
                elif ot_diff < -1.0:
                    away_wins = 1
                    home_OTLs = 1
                else:
                    # game goes to a shootout
                    flip = np.random.uniform(0,1,1)

                    if flip[0] > 0.5:
                        home_wins = 1
                        away_SOLs = 1
                    else:
                        away_wins = 1
                        home_SOLs = 1
               
         
        return home_goals, away_goals, home_wins, away_wins, home_OTLs, away_OTLs, home_SOLs, away_SOLs

    def simulate_game_poisson(self, home_gf_neut, home_ga_neut, away_gf_neut, away_ga_neut, home_b2b, away_b2b, is_playoffs):
        home_sched_boost = 0
        
        if home_b2b and away_b2b:
            home_sched_boost = 0.014
        elif not home_b2b and not away_b2b:
            home_sched_boost = 0
        elif home_b2b and not away_b2b:
            home_sched_boost = -0.012
        else:
            home_sched_boost = 0.03
        
        events = self.get_game_event_times(3.12)

        home_goals = 0
        away_goals = 0

        home_running_goals = []
        away_running_goals = []
        for event in events:
            home_gf = np.random.normal(home_gf_neut, self.GOAL_SD *2.25, 1) * (1 + home_sched_boost / 2.0 + self.HOME_ICE_AD / 2.0 ) 
            home_ga = np.random.normal(home_ga_neut, self.GOAL_SD *2.25, 1) / (1 + home_sched_boost / 2.0 + self.HOME_ICE_AD / 2.0 ) 

            away_gf = np.random.normal(away_gf_neut, self.GOAL_SD *2.25, 1) / (1 + home_sched_boost / 2.0 + self.HOME_ICE_AD / 2.0 ) 
            away_ga = np.random.normal(away_ga_neut, self.GOAL_SD *2.25, 1) * (1 + home_sched_boost / 2.0 + self.HOME_ICE_AD / 2.0 ) 

            if home_gf > away_gf and home_ga < away_gf:
                home_goals = home_goals + 1
            elif home_gf < away_gf and home_ga > away_gf:
                away_goals = away_goals +1

            home_running_goals.append(home_goals)
            away_running_goals.append(away_goals)

        game_chart = pd.DataFrame({'iat':[0] + events + [60], 'homeG':[0] + home_running_goals + [home_goals], 'awayG':[0]+away_running_goals+[away_goals]})

        home_wins = 0
        away_wins = 0
        home_OTLs = 0
        away_OTLs = 0
        home_SOLs = 0
        away_SOLs = 0

        if home_goals != away_goals:
            if home_goals > away_goals:
                home_goals = home_goals + 1
                home_wins = 1
            else:
                away_goals = away_goals + 1
                away_wins = 1
        else:
            if not is_playoffs:
                # game goes to OT
                home_gf_ot = np.random.normal(home_gf_neut, self.GOAL_SD, 1) * (1 + home_sched_boost + self.HOME_ICE_AD)
                home_ga_ot = np.random.normal(home_ga_neut, self.GOAL_SD, 1) / (1 + home_sched_boost + self.HOME_ICE_AD)

                away_gf_ot = np.random.normal(away_gf_neut, self.GOAL_SD, 1) / (1 + home_sched_boost + self.HOME_ICE_AD)
                away_ga_ot = np.random.normal(away_ga_neut, self.GOAL_SD, 1) * (1 + home_sched_boost + self.HOME_ICE_AD)

                home_goals_ot = (home_gf_ot + away_ga_ot) / 2.0
                away_goals_ot = (home_ga_ot + away_gf_ot) / 2.0

                ot_diff = home_goals_ot - away_goals_ot

                if ot_diff > 1:
                    home_wins = 1
                    away_OTLs = 1
                elif ot_diff < -1.0:
                    away_wins = 1
                    home_OTLs = 1
                else:
                    # game goes to a shootout
                    flip = np.random.uniform(0,1,1)

                    if flip[0] > 0.5:
                        home_wins = 1
                        away_SOLs = 1
                    else:
                        away_wins = 1
                        home_SOLs = 1
            else:
                # playoffs have no ties or shootouts
                home_gf_ot = np.random.normal(home_gf_neut, self.GOAL_SD, 1) * (1 + home_sched_boost + self.HOME_ICE_AD)
                home_ga_ot = np.random.normal(home_ga_neut, self.GOAL_SD, 1) / (1 + home_sched_boost + self.HOME_ICE_AD)

                away_gf_ot = np.random.normal(away_gf_neut, self.GOAL_SD, 1) / (1 + home_sched_boost + self.HOME_ICE_AD)
                away_ga_ot = np.random.normal(away_ga_neut, self.GOAL_SD, 1) * (1 + home_sched_boost + self.HOME_ICE_AD)

                home_goals_ot = (home_gf_ot + away_ga_ot) / 2.0
                away_goals_ot = (home_ga_ot + away_gf_ot) / 2.0   
            
                if(home_goals_ot > away_goals_ot):
                    home_goals = home_goals + 1
                    home_wins = 1
                else:
                    away_goals = away_goals + 1
                    away_wins = 1          
         
        return home_goals, away_goals, home_wins, away_wins, home_OTLs, away_OTLs, home_SOLs, away_SOLs, game_chart

    def get_game_event_times(self, lam):
        events = np.random.poisson(lam, 20)
        df = pd.DataFrame({'iat':events})
        df['at'] = df['iat'].cumsum()
        filtered  = [ num for num in list(df['at']) if num < 60 ]
        return filtered



