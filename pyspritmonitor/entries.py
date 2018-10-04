import json
import pandas as pd


class Entries:
    df = pd.DataFrame()

    """Base class for entries"""
    def _read_csv(self, csv, json_in_note, time_columns):
        """Read entries exported as CSV"""
        df = pd.read_csv(csv, sep=';', index_col='Date', parse_dates=[0], dayfirst=True,
                         decimal=',', escapechar='\\')
        df.sort_index(axis=0, ascending=True, inplace=True)  # Reverse by rows
        if json_in_note:
            df = self._convert_json_columns(df, 'Note')
        if time_columns:
            df = self._convert_time_columns(df, time_columns)
        return df

    @staticmethod
    def _convert_json_columns(df, columns):
        """Convert JSON from selected columns to separate columns"""
        df = df.join(df[columns].dropna().apply(json.loads).apply(pd.Series))
        df.drop(columns, 1, inplace=True)
        return df

    @staticmethod
    def _convert_time_columns(df, columns):
        """Convert string in format MM:HH:SS to Timedelta"""
        df[columns] = df[columns].apply(pd.to_timedelta)
        return df

    def to_csv(self, path):
        import os
        directory = os.path.dirname(path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        self.df.to_csv(path)
