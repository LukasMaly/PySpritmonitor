import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from .entries import Entries


class Fuelings(Entries):
    """Class for fuelings entries"""
    def __init__(self, csv, json_in_note=False, time_columns=None):
        self.__df_original = super()._read_csv(csv, json_in_note, time_columns)
        self.__df_formatted = self._format(self.__df_original[:])
        self.df = self._calculate(self.__df_formatted[:])

    def _format(self, df):
        """Format fueling numeric columns"""
        df = self._numerics_to_strings(df)
        df = self._roads_to_columns(df)
        return df

    @staticmethod
    def _numerics_to_strings(df):
        """Format fueling numeric columns to their string representation"""
        from .formats import formats
        columns_to_format = ['Type', 'Tires', 'Roads', 'Driving style', 'Fuel']
        for column_name in columns_to_format:
            df[column_name] = df[column_name].apply(
                lambda x: formats['Fuelings'][column_name][x]
            )
        return df

    @staticmethod
    def _roads_to_columns(df):
        """Separate road types to individual columns"""
        loc = df.columns.get_loc('Roads') + 1
        for road in ['motor-way', 'city', 'country roads']:
            df.insert(loc, road.capitalize(), df['Roads'].str.contains(road))
            loc += 1
        del df['Roads']
        return df

    def _calculate(self, df):
        """Calculate new variables from available variables"""
        df = self._calculate_unit_price(df)
        return df

    @staticmethod
    def _calculate_unit_price(df):
        """Calculate fuel unit price based on total price and quantity"""
        unit_price = df['Total price'] / df['Quantity']
        unit_price = unit_price.round(1)  # round to one decimal
        df.insert(5, 'Unit price', unit_price)
        return df

    def get_summary(self):
        """Return summary row"""
        import pandas as pd
        summary = pd.Series(self.df[['Quantity', 'Total price', 'BC-Time']].sum())
        summary = summary.append(pd.Series(self.df[['Unit price', 'Consumption', 'BC-Consumption', 'BC-Speed', 'BC-DriveGreen']].iloc[1:, ].apply(lambda x: np.average(x, weights=self.df['Trip'].iloc[1:].values))))
        return summary

    def plot_date_odometer(self):
        self.df['Odometer'].plot(title='Odometer', legend=False)
        plt.ylabel('Odometer (km)')
        sns.set()
        plt.show(block=False)

    def plot_date_trip(self):
        self.df['Trip'].plot(kind='bar', title='Trip', legend=False, edgecolor='k')
        xtl = self.df['Trip'].index.map(lambda t: t.strftime('%Y-%m-%d'))
        plt.xticks(range(len(self.df['Trip'])), xtl, rotation=30)
        plt.xlabel('Date')
        plt.ylabel('Trip (km)')
        sns.set()
        plt.show(block=False)

    def plot_date_trip_cum(self):
        blank = self.df['Trip'].cumsum().shift(1).fillna(0)
        plot = self.df['Trip'].plot(kind='bar', title='Trip', legend=False, stacked=True, bottom=blank, edgecolor='k')
        plot.hlines(blank.values, range(-1, len(blank)-1), range(0, len(blank)), linewidth=1)
        sns.set()
        plt.show(block=False)

    def plot_date_quantity(self):
        self.df['Quantity'].plot(kind='bar', title='Fuel quantity', legend=False, edgecolor='k')
        plt.ylabel('Quantity (l)')
        plt.ylim(ymin=0)
        sns.set()
        plt.show(block=False)

    def plot_date_totalprice(self):
        self.df['Total price'].plot(kind='bar', title='Fuel total price', legend=False, edgecolor='k')
        plt.ylabel('Total price (' + self.df['Currency'][0] + ')')
        plt.ylim(ymin=0)
        sns.set()
        plt.show(block=False)

    def plot_date_unitprice(self):
        self.df['Unit price'].plot(kind='bar', title='Fuel unit price', legend=False, edgecolor='k')
        plt.ylabel('Unit price (' + self.df['Currency'][0] + ')')
        plt.ylim(ymin=0)
        sns.set()
        plt.show(block=False)

    def plot_date_consumption(self):
        self.df['Consumption'].plot(kind='bar', title='Fuel consumption', legend=False, edgecolor='k')
        plt.ylabel('Consumption (l/100 km)')
        plt.ylim(ymin=0)
        sns.set()
        plt.show(block=False)
