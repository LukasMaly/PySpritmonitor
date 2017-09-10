import json
import pandas as pd


class Costs():
    def __init__(self, filepath, json_in_note=False):
        self.df = self.__read_costs_csv(filepath, json_in_note)

    def __read_costs_csv(self, filepath, json_in_note):
        """Read costs exported as CSV"""
        df = pd.read_csv(filepath, sep=';', parse_dates=[0], dayfirst=True,
                         decimal=',', escapechar='\\')
        if json_in_note:
            df = self.__convert_json_columns(df, 'Note')
        return df

    def __convert_json_columns(self, df, columns):
        """Convert JSON from selected columns to separate columns"""
        df = df.join(df[columns].dropna().apply(json.loads).apply(pd.Series))
        df.drop(columns, 1, inplace=True)
        return df
