import dataclasses
import typing as typ
import pathlib
import datetime
import csv
import numpy as np

__all__ = ['confirmed_global_filename', 'Dataset', 'read']

base_path = pathlib.Path(__file__).parent.parent / 'csse_covid_19_data/csse_covid_19_time_series'
confirmed_global_filename = base_path / pathlib.Path('time_series_covid19_confirmed_global.csv')
confirmed_us_filename = base_path / pathlib.Path('time_series_covid19_confirmed_US.csv')


@dataclasses.dataclass
class Dataset:

    dates: typ.List[str]
    states: typ.List[str]
    countries: typ.List[str]
    latitudes: np.ndarray
    longitudes: np.ndarray
    data: np.ndarray


class axis:

    space = 0
    time = 1


def read(path: pathlib.Path, is_us=False):

    if not is_us:
        class column:
            state = 0
            country = 1
            latitude = 2
            longitude = 3
            data = slice(4, None)
    else:
        class column:
            state = 6
            country = 7
            latitude = 8
            longitude = 9
            data = slice(11, None)

    states = []
    countries = []
    latitudes = []
    longitudes = []
    data = []

    with open(str(path), 'r') as f:

        reader = csv.reader(f)

        for i, row in enumerate(reader):

            if i == 0:
                dates = row[column.data]

            else:
                states.append(row[column.state])
                countries.append(row[column.country])
                latitudes.append(row[column.latitude])
                longitudes.append(row[column.longitude])
                data.append(row[column.data])

    latitudes = np.array(latitudes, dtype=np.float)
    longitudes = np.array(longitudes, dtype=np.float)
    data = np.array(data, dtype=np.int)

    return Dataset(dates, states, countries, latitudes, longitudes, data)


def test_read():

    dataset = read(confirmed_global_filename)

    assert isinstance(dataset, Dataset)
