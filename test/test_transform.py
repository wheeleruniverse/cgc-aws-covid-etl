# internal modules
import classes
import transform

# external modules
import pandas
import unittest


class TestTransform(unittest.TestCase):
    """class containing unit tests for transform.py"""

    def test_transform1(self):
        """
        :return: pass or fail if the transform method works with ds1 and ds2
        """
        print("test_transform1")
        ds1_headers = ["date", "col1", "col2"]
        ds1 = create_dataset("ds1", ds1_headers, "date")
        ds1.df = pandas.DataFrame(columns=ds1_headers)
        ds1.df.loc[0] = pandas.Series({"date": "2020-09-11", "col1": "test1", "col2": "test"})
        ds1.df.loc[1] = pandas.Series({"date": "2020-09-15", "col1": "test2", "col2": "test"})
        ds1.df.loc[2] = pandas.Series({"date": "2020-09-18", "col1": "test3", "col2": "test"})

        ds2_headers = ["DateString", "Name"]
        ds2 = create_dataset("ds2", ds2_headers, "DateString")
        ds2.df = pandas.DataFrame(columns=ds2_headers)
        ds2.df.loc[0] = pandas.Series({"DateString": "2020-09-12", "Name": "Test1"})
        ds2.df.loc[1] = pandas.Series({"DateString": "2020-09-18", "Name": "Test2"})

        # TODO: Is this a problem
        result = transform.transform(ds1, ds2)
        self.assertEqual(len(result), 1)

        stat = result[0]
        self.assertIsNotNone(stat)
        self.assertIsInstance(stat, classes.CovidStat)
        self.assertEqual(stat.idx, 0)
        self.assertEqual(str(stat.date), "2020-09-18 00:00:00")
        self.assertIsNone(stat.cases, None)
        self.assertIsNone(stat.deaths, None)
        self.assertIsNone(stat.recovered, None)

    def test_transform2(self):
        """
        :return: pass or fail if the transform method works with ds1
        """
        print("test_transform2")
        ds1_headers = ["date", "col1", "col2"]
        ds1 = create_dataset("ds1", ds1_headers, "date")
        ds1.df = pandas.DataFrame(columns=ds1_headers)
        ds1.df.loc[0] = pandas.Series({"date": "2020-09-11", "col1": "test1", "col2": "test"})
        ds1.df.loc[1] = pandas.Series({"date": "2020-09-15", "col1": "test2", "col2": "test"})
        ds1.df.loc[2] = pandas.Series({"date": "2020-09-18", "col1": "test3", "col2": "test"})

        result = transform.transform(ds1, None)
        self.assertEqual(len(result), 3)

        idx = 0
        for stat in result:
            self.assertIsNotNone(stat)
            self.assertIsInstance(stat, classes.CovidStat)
            self.assertEqual(stat.idx, idx)
            self.assertEqual(str(stat.date), f"{ds1.df.loc[idx][0]} 00:00:00")
            self.assertIsNone(stat.cases, None)
            self.assertIsNone(stat.deaths, None)
            self.assertIsNone(stat.recovered, None)
            idx += 1

    def test_transform3(self):
        """
        :return: pass or fail if the transform method fails without ds1
        """
        print("test_transform3")

        try:
            transform.transform(None, None)
            self.fail("Expected ValueError was not raised")

        except ValueError as e:
            self.assertEqual(str(e), "'ds1.df' could not be extracted")


def create_dataset(name, headers, match):
    """
    creates a dataset with the provided parameters
    :param name: the name to set
    :param headers: the headers to set for headers_all and headers_key
    :param match: the match_field to set
    :return: the created Dataset
    """

    dataset = classes.Dataset(name)
    dataset.headers_all = headers
    dataset.headers_key = headers
    dataset.match_field = match
    return dataset


if __name__ == '__main__':
    unittest.main()
