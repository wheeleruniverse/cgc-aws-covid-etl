
# -------------------------------
# internal modules
import classes

# -------------------------------
# external modules
import pandas as pd
from dateutil.parser import parse


def transform(ds1, ds2):
    """
    transforms the dataframes provided into CovidStat instances
    :param ds1: the primary Dataset Instance to use; None will cause a ValueError
    :param ds2: the secondary Dataset Instance to use; None will cause ds1 to be used solely
    :return: created CovidStat instances
    """

    ds1_df = ds1.df if ds1 is not None else None
    ds2_df = ds2.df if ds2 is not None else None
    tar_df = ds1_df

    # merge dataframes
    if ds1_df is None:
        raise ValueError("'ds1.df' could not be extracted")

    if ds2_df is None:
        print("WARN: 'ds2.df' could not be extracted")

    elif ds1.match_field is not None and ds2.match_field is not None:
        tar_df = pd.merge(ds1_df, ds2_df, left_on=ds1.match_field, right_on=ds2.match_field)

    print(f"'tar_df':\n{tar_df}")

    # convert dataframe to CovidStat instances
    stats = list()
    for i, r in tar_df.iterrows():
        cs = classes.CovidStat(i)
        cs.cases = r["cases"] if "cases" in r else None
        cs.deaths = r["deaths"] if "deaths" in r else None
        cs.recovered = r["Recovered"] if "Recovered" in r else None

        try:
            cs.date = parse_date(r["date"]) if "date" in r else None

        except TypeError:
            print(f"WARN: could not parse 'date' for row #{i} of 'tar_df'\n\t'date': {r['date']}")
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
