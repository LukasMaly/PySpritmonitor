import json
import pandas as pd


class Fuelings:
    def __init__(self, filepath, json_in_note=True, time_columns='BC-Time'):
        self.__df = self.__read_fuelings_csv(filepath, json_in_note, time_columns)
        self.__calculate_unit_price()

    def __read_fuelings_csv(self, filepath, json_in_note=False,
                          time_columns=None):
        """Read fueling entries exported as CSV"""
        df = pd.read_csv(filepath, sep=';', parse_dates=[0], dayfirst=True,
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

    @staticmethod
    def __get_formatted(df):
        """Format fueling numeric columns to their string representation"""
        from pyspritmonitor.formats import formats
        columns_to_format = ['Type', 'Tires', 'Roads', 'Driving style', 'Fuel']
        for column_name in columns_to_format:
            df[column_name] = df[column_name].apply(
                lambda x: formats['Fuelings'][column_name][x]
            )
        return df

    def __calculate_unit_price(self):
        unit_price = self.__df['Total price'] / self.__df['Quantity']
        self.__df.insert(5, 'Unit price', unit_price)

    def get_df(self, formatted=True):
        if formatted:
            df = self.__get_formatted(self.__df[:])
        else:
            df = self.__df
        return df
