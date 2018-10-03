# PySpritmonitor

Python package for reading Spritmonitor.de's CSV data.

## Usage

Either pass paths to CSV files stored locally or obtain data directly from Spritmonitor.de by providing login credentials and vehicle's ID.

### CSVs stored locally

Export the fueling and cost entries from https://www.spritmonitor.de/ as CSV files.

Import classes `Costs` and `Fuelings` from `pyspritmonitor` module.

```Python
from pyspritmonitor import Costs, Fuelings
```

Pass path to CSV file as argument to `Costs` and `Fuelings`.

```Python
costs = Costs('data/853999_costs.csv')
fuelings = Fuelings('data/853999_fuelings.csv')
```

Then you can access data as DataFrame type:

```Python
print(costs.df)
print(fuelings.df)
```

### Obtain data from Spritmonitor.de

Import class `Login` from `pyspritmonitor` module.

```Python
from pyspritmonitor import Login, Costs, Fuelings
```

Provide class instance with your username, password and vehicle's ID.

```Python
login = Login(username='MyUsername', password='MyPassword', vehicle_id='999999')
```

Then pass class `Login` variables `costs_csv` and `fuelings_csv` to classes `Costs` and `Fuelings`.

```Python
costs = Costs(login.costs_csv)
fuelings = Fuelings(login.fuelings_csv)
```

The rest remains same as when accessing CSVs stored locally described above.

### JSON in Note

You can pack JSON objects into Spritmonitor's 'Note' field and then unpack it by using argument `json_in_note=True`: 

```Python
fuelings = Fuelings(fuelings_path, json_in_note=True)
```

Each variable is then converted into separate column.

### Time variables

If some of the columns contain time, you can convert them to Timedelta types by passing their names to parameter `time_columns`:

```Python
fuelings = Fuelings(fuelings_path, json_in_note=True, time_columns='BC-Time')
```
