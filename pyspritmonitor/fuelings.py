from .entries import Entries


class Fuelings(Entries):
    """Class for fuelings entries"""
    def __init__(self, filepath, json_in_note=False, time_columns=None):
        self.__df_original = super()._read_csv(filepath, json_in_note, time_columns)
        self.__df_formatted = self.__format(self.__df_original[:])
        self.df = self.__calculate(self.__df_formatted[:])

    def __format(self, df):
        "Format fueling numeric columns"
        df = self.__numerics_to_strings(df)
        df = self.__roads_to_columns(df)
        return df

    @staticmethod
    def __numerics_to_strings(df):
        """Format fueling numeric columns to their string representation"""
        from .formats import formats
        columns_to_format = ['Type', 'Tires', 'Roads', 'Driving style', 'Fuel']
        for column_name in columns_to_format:
            df[column_name] = df[column_name].apply(
                lambda x: formats['Fuelings'][column_name][x]
            )
        return df

    @staticmethod
    def __roads_to_columns(df):
        """Separate road types to individual columns"""
        loc = df.columns.get_loc('Roads') + 1
        for road in ['motor-way', 'city', 'country roads']:
            df.insert(loc, road.capitalize(), df['Roads'].str.contains(road))
            loc += 1
        del df['Roads']
        return df

    def __calculate(self, df):
        """Calculate new variables from available variables"""
        df = self.__calculate_unit_price(df)
        return df

    @staticmethod
    def __calculate_unit_price(df):
        """Calculate fuel unit price based on total price and quantity"""
        unit_price = df['Total price'] / df['Quantity']
        df.insert(5, 'Unit price', unit_price)
        return df
