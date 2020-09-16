import pandas as pd


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
