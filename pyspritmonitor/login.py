from io import StringIO
import requests


class Login:
    """Class for reading CSVs directly from Spritmonitor.de"""
    def __init__(self, username, password, vehicle_id):
        s = requests.Session()
        data = {'username': username,
                'password': password}
        s.post('https://www.spritmonitor.de/en/login.html', data=data)

        self.costs_csv = StringIO(s.get(
            'https://www.spritmonitor.de/en/costs_notes/' + vehicle_id
            + '/csvexport.csv').text)
        self.fuelings_csv = StringIO(s.get(
            'https://www.spritmonitor.de/en/fuelings/' + vehicle_id
            + '/csvexport.csv').text)
