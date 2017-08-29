import pandas as pd


class Costs():
    def __init__(self, filepath):
        self.__df = self.__read_costs_csv(filepath)

    def __read_costs_csv(self, filepath):
        """Read costs exported as CSV"""
        df = pd.read_csv(filepath, sep=';', parse_dates=[0], dayfirst=True,
                         decimal=',', escapechar='\\')
        return df

    def get_df(self):
        df = self.__df
        return df
