import pandas as pd
from dateutil.parser import parse


class CovidStat:
    """class to store a COVID-19 Statistic"""

    def __init__(self, idx):
        """
        initializes a CovidStat instance
        :param idx: the idx to set
        """
        self.idx = idx
        self.cases = None
        self.date = None
        self.deaths = None
        self.recovered = None

    def to_string(self):
        """
        :return: this CovidStat instance as a String
        """
        return f"CovidStat[" \
               f"idx: {self.idx}, " \
               f"date: {self.date}, " \
               f"cases: {self.cases}, " \
               f"deaths: {self.deaths}, " \
               f"recovered: {self.recovered}" \
               f"]"


class Dataset:
    """class to track key information for a single set of data"""

    def __init__(self, name):
        """initializes a Dataset instance"""

        self.name = name
        self.df = None
        self.headers_all = None
        self.headers_key = None
        self.match_field = None
        self.source_url = None


def extract(url, columns=None, filter_key=None, filter_val=None):
    """
    extracts data for COVID-19 Statistics from reputable sources
    :param url: the url to download from
    :param columns: the columns to keep, or None to provide all
    :param filter_key: the column to match on and filter records, or None to not filter
    :param filter_val: the value the filter_key column should be to retain the records, or None to not filter
    :return: a pandas dataframe of the downloaded source or None
    """

    try:
        # create dataframe
        df = pd.read_csv(url)
        print(f"DEBUG: From Source: {df.shape}")

        # filter dataframe columns
        if columns is not None:
            df = df.filter(columns)
            print(f"DEBUG: Filter Column(s) by {columns}: {df.shape}")

        # filter dataframe records
        if filter_key is not None and filter_val is not None:
            df = df[df[filter_key] == filter_val]
            del df[filter_key]
            print(f"DEBUG: Filter Records(s) by [{filter_key}=={filter_val}]: {df.shape}")

        return df

    except ValueError as e:
        print(f"ERROR: {e}")
        return None


def transform(ds1, ds2):
    """
    transforms the dataframes provided into CovidStat instances
    :param ds1: the primary Dataset Instance to use; None will cause a ValueError
    :param ds2: the secondary Dataset Instance to use; None will cause ds1 to be used solely
    :return: created CovidStat instances
    """

    # merge dataframes
    if ds1.df is None:
        raise ValueError("'ds1.df' could not be extracted")

    if ds2.df is None:
        print("WARN: 'ds2.df' could not be extracted")
        target_df = ds1.df

    else:
        target_df = pd.merge(ds1.df, ds2.df, left_on=ds1.match_field, right_on=ds2.match_field)

    print(f"'target_df':\n{target_df}")

    # convert dataframe to CovidStat instances
    stats = list()
    for i, r in target_df.iterrows():
        cs = CovidStat(i)
        cs.cases = r["cases"] if "cases" in r else None
        cs.deaths = r["deaths"] if "deaths" in r else None
        cs.recovered = r["Recovered"] if "Recovered" in r else None

        try:
            cs.date = parse_date(r["date"]) if "date" in r else None

        except TypeError:
            print(f"WARN: could not parse 'date' for row #{i} of 'target_df'\n\t'date': {r['date']}")
            continue

        stats.append(cs)

    return stats


def parse_date(date_string):
    """
    attempts to parse a string into a date
    :param date_string: the string representation of a date
    :return: the parsed date or None
    """
    try:
        return parse(date_string)

    except (OverflowError, ValueError) as e:
        print(f"WARN: {e}")
        return None


if __name__ == "__main__":

    # define ny_dataset
    ny_dataset = Dataset("ny_dataset")
    ny_dataset.headers_all = ["date", "cases", "deaths"]
    ny_dataset.headers_key = ny_dataset.headers_all
    ny_dataset.match_field = "date"
    ny_dataset.source_url = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv"

    # extract and print ny_dataset
    ny_dataset.df = extract(ny_dataset.source_url)
    print(f"'ny_dataset.df':\n{ny_dataset.df}")

    # define jh_dataset
    jh_dataset = Dataset("jh_dataset")
    jh_dataset.headers_all = [
        "Date", "Country/Region", "Province/State", "Lat", "Long", "Confirmed", "Recovered", "Deaths"
    ]
    jh_dataset.headers_key = ["Date", "Country/Region", "Recovered"]
    jh_dataset.match_field = "Date"
    jh_dataset.source_url = \
        "https://raw.githubusercontent.com/datasets/covid-19/master/data/time-series-19-covid-combined.csv"

    # extract and print jh_dataset
    jh_dataset.df = extract(jh_dataset.source_url, jh_dataset.headers_key, "Country/Region", "US")
    print(f"'jh_dataset.df':\n{jh_dataset.df}")

    # transform the datasets into CovidStat Instances
    covid_stats = transform(ny_dataset, jh_dataset)

    # print CovidStats
    for stat in covid_stats:
        print(stat.to_string())


