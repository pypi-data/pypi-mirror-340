'''Teams Endpoint'''
import os
import pandas as pd

from dans.endpoints._base import Endpoint

class Teams(Endpoint):
    '''Endpoint for finding teams with defensive strength that falls within a desired range'''

    expected_columns = [
        "SEASON",
        "TEAM",
        "DRTG",
        "OPP_TS"
    ]

    def __init__(
        self,
        year_range,
        drtg_range
    ):
        self.year_range = year_range
        self.drtg_range = drtg_range
        self.path = None

    def bball_ref(self):
        '''Reads bball-ref team data and return teams that falls within self.drtg_range'''
        self.path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                     'data\\bball-ref-teams.csv')
        return self._read_path()

    def nba_stats(self):
        '''Reads nba-stats team data and return teams that falls within self.drtg_range'''
        self.path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                     'data\\nba-stats-teams.csv')
        return self._read_path()

    def _read_path(self):
        teams_df = pd.read_csv(self.path).drop(columns="Unnamed: 0")
        teams_df = teams_df[
            (teams_df["SEASON"] >= self.year_range[0]) &
            (teams_df["SEASON"] <= self.year_range[1]) &
            (teams_df["DRTG"] >= self.drtg_range[0]) &
            (teams_df["DRTG"] <= self.drtg_range[1])]

        return teams_df
