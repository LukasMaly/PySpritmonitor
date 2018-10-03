from .entries import Entries


class Costs(Entries):
    """Class for costs entries"""
    def __init__(self, csv, json_in_note=False, time_columns=None):
        self.df = super()._read_csv(csv, json_in_note, time_columns)
