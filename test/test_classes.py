# internal modules
import classes

# external modules
import datetime
import pandas
import unittest


class TestClasses(unittest.TestCase):
    """class containing unit tests for classes.py"""

    def test_CovidStatTableName(self):
        """
        :return: pass or fail if the CovidStat table name matches the expectation
        """
        print("test_CovidStatTableName")
        self.assertEqual(classes.CovidStat.table_name, "CovidStats")

    def test_CovidStatConstructor(self):
        """
        :return: pass or fail if the constructor is working as expected
        """
        print("test_CovidStatConstructor")
        instance = classes.CovidStat(1)
        self.assertIsNotNone(instance)
        self.assertIsInstance(instance, classes.CovidStat)

    def test_CovidStatFields(self):
        """
        :return: pass or fail if the expected fields can be set and read
        """
        print("test_CovidStatFields")
        num = 1
        now = datetime.datetime.now()
        obj = classes.CovidStat(num)
        obj.cases = num
        obj.date = now
        obj.deaths = num
        obj.recovered = num

        self.assertEqual(obj.idx, 1)
        self.assertEqual(obj.cases, 1)
        self.assertEqual(obj.date, now)
        self.assertEqual(obj.deaths, 1)
        self.assertEqual(obj.recovered, 1)

    def test_CovidStatToString(self):
        """
        :return: pass or fail if the CovidStat instance prints the to_string returns a properly formatted String
        """
        print("test_CovidStatToString")
        num = 1
        now = datetime.datetime.now()
        obj = classes.CovidStat(num)
        obj.cases = num
        obj.date = now
        obj.deaths = num
        obj.recovered = num

        expected = f"CovidStat[idx: 1, date: {now}, cases: 1, deaths: 1, recovered: 1]"
        self.assertEqual(obj.to_string(), expected)

    def test_DatasetConstructor(self):
        """
        :return: pass or fail if the constructor is working as expected
        """
        print("test_DatasetConstructor")
        instance = classes.Dataset("TestDataset")
        self.assertIsNotNone(instance)
        self.assertIsInstance(instance, classes.Dataset)

    def test_DatasetFields(self):
        """
        :return: pass or fail if the constructor is working as expected
        """
        print("test_DatasetFields")
        name = "TestDataset"
        df = pandas.DataFrame()
        headers_all = ["Test1", "Test2"]
        headers_key = ["Test1"]
        match_field = "Test1"
        source_url = "http://example.com"

        obj = classes.Dataset(name)
        obj.df = df
        obj.headers_all = headers_all
        obj.headers_key = headers_key
        obj.match_field = match_field
        obj.source_url = source_url

        self.assertEqual(obj.name, name)
        self.assertEqual(obj.df.shape, df.shape)
        self.assertEqual(obj.headers_all, headers_all)
        self.assertEqual(obj.headers_key, headers_key)
        self.assertEqual(obj.match_field, match_field)
        self.assertEqual(obj.source_url, source_url)


if __name__ == '__main__':
    unittest.main()
