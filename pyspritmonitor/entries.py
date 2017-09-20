import json
import pandas as pd


class Entries:
    """Base class for entries"""
    def _read_csv(self, csv, json_in_note, time_columns):
        """Read entries exported as CSV"""
        df = pd.read_csv(csv, sep=';', parse_dates=[0], dayfirst=True,
                         decimal=',', escapechar='\\')
        if json_in_note:
            df = self.__convert_json_columns(df, 'Note')
        if time_columns:
            df = self.__convert_time_columns(df, time_columns)
        return df

    def __convert_json_columns(self, df, columns):
        """Convert JSON from selected columns to separate columns"""
        df = df.join(df[columns].dropna().apply(json.loads).apply(pd.Series))
        df.drop(columns, 1, inplace=True)
        return df

    def __convert_time_columns(self, df, columns):
        """Convert string in format MM:HH:SS to Timedelta"""
        df[columns] = df[columns].apply(pd.to_timedelta)
        return df
