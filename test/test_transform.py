# internal modules
import classes
import transform

# external modules
import unittest


class TestTransform(unittest.TestCase):
    """class containing unit tests for transform.py"""

    def test_transform(self):
        """
        :return: pass or fail if the transform method works
        """
        print("test_transform")

        # expected = (31, 3)
        # df = extract.extract(data_sample_url)
        # self.assertEqual(df.shape, expected)


def create_random_dataset():



    # ny_dataset = classes.Dataset("ny_dataset")
    # ny_dataset.headers_all = ["date", "cases", "deaths"]
    # ny_dataset.headers_key = ny_dataset.headers_all
    # ny_dataset.match_field = "date"
    # ny_dataset.source_url = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv"
    #
    # # extract and print ny_dataset
    # ny_dataset.df = extract.extract(ny_dataset.source_url)
    # print(f"'ny_dataset.df':\n{ny_dataset.df}")


if __name__ == '__main__':
    unittest.main()
