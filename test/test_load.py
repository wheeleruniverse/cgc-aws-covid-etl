# internal modules
import load

# external modules
import datetime
import marshmallow_dataclass
import random
import unittest


epoch = datetime.datetime.utcfromtimestamp(0)


@marshmallow_dataclass.dataclass
class CovidStatTest:
    """class to test data load logic into a secondary table"""

    table_name = "CovidStatsTest"

    idx: int
    cases: int
    date: str
    deaths: int
    expiry: int

    def __init__(self):
        """constructs a CovidStatTest instance"""


class TestLoad(unittest.TestCase):
    """class containing unit tests for load.py"""

    def test_load(self):
        """
        :return: pass or fail if the ...
        """
        print("test_load")
        size = 25
        sample_date = list()
        for _ in range(size):
            sample_date.append(create_random_instance())

        load_response = load.load_all(CovidStatTest, sample_date)
        self.assertEqual(len(load_response), size)


def create_random_instance():
    """
    creates a CovidStatTest instance with random values
    :return: the newly created CovidStatTest instance
    """
    # find current date
    now = datetime.datetime.now()

    # generate random date
    beg_date = datetime.datetime(2019, 1, 1, 0, 0, 0, 0)
    end_date = now
    ran_date = beg_date + datetime.timedelta(seconds=random.randint(0, int((end_date - beg_date).total_seconds())))

    # create CovidStatTest instance
    inst = CovidStatTest()
    inst.idx = random.randint(1, 9999999)
    inst.cases = random.randint(1, 9999999)
    inst.date = ran_date
    inst.deaths = random.randint(1, 9999999)
    inst.expiry = unix_epoch(now + datetime.timedelta(days=5))
    return inst


def unix_epoch(dt):
    """
    calculates the datetime provided in unix epoch format
    :param dt: the datetime to process
    :return: the unix epoch representation
    """
    return (dt - epoch).total_seconds() * 1000.0


if __name__ == '__main__':
    unittest.main()
