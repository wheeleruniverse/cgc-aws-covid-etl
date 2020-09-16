import pandas as pd
from dateutil import parser


class CovidStat:
    """class to store a COVID-19 Statistic"""

    def __init__(self, idx, date, cases, deaths):
        """
        initializes a CovidStat instance
        :param idx: the idx to set
        :param date: the date to set
        :param cases: the cases to set
        :param deaths: the deaths to set
        """

        self.idx = idx
        self.date = CovidStat.parse_date(date)
        self.cases = cases
        self.deaths = deaths

    def get_idx(self):
        """
        :return: the idx set
        """
        return self.idx

    def get_date(self):
        """
        :return: the date set
        """
        return self.date

    def get_cases(self):
        """
        :return: the cases set
        """
        return self.cases

    def get_deaths(self):
        """
        :return: the deaths set
        """
        return self.deaths

    def to_string(self):
        """
        :return: this CovidStat instance as a String
        """
        return f"CovidStat[idx: {self.idx}, date:{self.date}, cases:{self.cases}, deaths:{self.deaths}]"

    @staticmethod
    def parse_date(date_string):
        """
        attempts to parse a string into a date
        :param date_string: the string representation of a date
        :return: the parsed date or None
        """
        try:
            return parser.parse(date_string)

        except (OverflowError, ValueError) as e:
            print(f"WARN: {e}")
            return None


def extract(url, columns=None):
    """
    extracts data for COVID-19 Statistics from reputable sources
    :param url: the url to download from
    :param columns: the columns to keep, or None to provide all
    :return: a pandas dataframe of the downloaded source or None
    """

    try:
        # create dataframe
        df = pd.read_csv(url)

        # filter dataframe by columns
        if columns is not None:
            df = df.filter(columns)

        return df

    except ValueError as e:
        print(f"ERROR: {e}")
        return None


def transform(ny_df, jh_df):

    stats = list()
    for i, r in ny_df.iterrows():
        stats.append(CovidStat(i, r["date"], r["cases"], r["deaths"]))

    for r in stats:
        print(r.to_string())


class Deaths(object):
    pass


if __name__ == "__main__":

    # define sources

    # headers: date,cases,deaths
    ny_url = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv"
    ny_df = extract(ny_url)

    # headers: Date, Country / Region, Province / State, Lat, Long, Confirmed, Recovered, Deaths
    jh_url = "https://raw.githubusercontent.com/datasets/covid-19/master/data/time-series-19-covid-combined.csv"
    jh_df = extract(jh_url, ["Date", "Recovered"])

    print("ny_df:")
    print(ny_df)

    print("=========================================================")
    print("jh_df:")
    print(jh_df)


