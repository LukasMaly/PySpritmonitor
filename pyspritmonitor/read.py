import pandas as pd
import pkg_resources
import json


def _format_fuelings(df):
    """Format fueling numeric columns to their string representation"""
    columns_to_format = ['Type', 'Tires', 'Roads', 'Driving style', 'Fuel']
    for column_name in columns_to_format:
        df[column_name] = df[column_name].apply(
            lambda x: _formats['Fuelings'][column_name][x]
        )
    return df


def _format_costs(df):
    """Format costs numeric column to its string representation"""
    df['Type'] = df['Type'].apply(
        lambda x: _formats['Costs']['Type'][x]
    )
    return df


def _convert_json_columns(df, columns):
    """Convert JSON from selected columns to separate columns"""
    df = df.join(df[columns].dropna().apply(json.loads).apply(pd.Series))
    df = df.drop(columns, 1)
    return df


def _convert_time_columns(df, columns):
    """Convert string in format MM:HH:SS to Timedelta"""
    df[columns] = df[columns].apply(pd.to_timedelta)
    return df


def read_fuelings_csv(filepath, formatted=True, json_columns=None,
                      time_columns=None):
    """Read fuelings exported as CSV"""
    df = pd.read_csv(filepath, sep=';', parse_dates=[0], dayfirst=True,
                     decimal=',', escapechar='\\')
    if formatted:
        df = _format_fuelings(df)
    if json_columns:
        df = _convert_json_columns(df, json_columns)
    if time_columns:
        df = _convert_time_columns(df, time_columns)
    return df


def read_costs_csv(filepath):
    """Read costs exported as CSV"""
    df = pd.read_csv(filepath, sep=';', parse_dates=[0], dayfirst=True,
                     decimal=',', escapechar='\\')
    return df


def _load_formats():
    """Read costs and fuelings formats defined in JSON"""
    resource_package = __name__
    resource_path = '/'.join(('resources', 'formats.json'))
    formats = json.load(pkg_resources.resource_stream(resource_package,
                                                 resource_path))
    return formats

_formats = _load_formats()
