# internal modules
import extract

# external modules
import unittest


data_sample_url = "resources/DataSample.csv"


class TestExtract(unittest.TestCase):
    """class containing unit tests for extract.py"""

    def test_extract1(self):
        """
        :return: pass or fail if the extract method works with url
        """
        print("test_extract1")
        expected = (31, 3)
        df = extract.extract(data_sample_url)
        self.assertEqual(df.shape, expected)

    def test_extract2(self):
        """
        :return: pass or fail if the extract method works with url and columns
        """
        print("test_extract2")
        expected = (31, 2)
        df = extract.extract(data_sample_url, columns=["date", "cases"])
        self.assertEqual(df.shape, expected)

    def test_extract3(self):
        """
        :return: pass or fail if the extract method works with url, filter_key, and filter_val
        """
        print("test_extract3")
        expected = (1, 2)
        df = extract.extract(data_sample_url, filter_key="date", filter_val="2020-03-01")
        self.assertEqual(df.shape, expected)

    def test_extract4(self):
        """
        :return: pass or fail if the extract method works with url, columns, filter_key, and filter_val
        """
        print("test_extract4")
        expected = (1, 1)
        df = extract.extract(data_sample_url, columns=["date", "cases"], filter_key="date", filter_val="2020-03-01")
        self.assertEqual(df.shape, expected)


if __name__ == '__main__':
    unittest.main()
