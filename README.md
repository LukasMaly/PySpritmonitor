# pyspritmonitor

Python package for reading Spritmonitor.de data exported as CSV

## Usage

Export the fueling and cost entries from https://www.spritmonitor.de/ as CSV files.

Import classes `Costs` and `Fuelings` from `pyspritmonitor` module.

```Python
from pyspritmonitor import Costs, Fuelings
```

Pass path to CSV file as argument to `Costs` or `Fuelings`.

```Python
costs = Costs('data/853999_costs.csv')
fuelings = Fuelings'data/853999_fuelings.csv')
```

Then you can access data as DataFrame type:

```Python
print(costs.df)
print(fuelings.df)
```

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
