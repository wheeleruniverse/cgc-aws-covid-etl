import marshmallow_dataclass
import marshmallow


@marshmallow_dataclass.dataclass
class CovidStat:
    """class to store a COVID-19 Statistic"""

    table_name = "CovidStats"

    idx: int
    cases: int
    date: marshmallow_dataclass.NewType("date", str, marshmallow.fields.Date)
    deaths: int
    recovered: int

    field = marshmallow.fields.Email

    def __init__(self, idx):
        """
        initializes a CovidStat instance
        :param idx: the idx to set
        """
        self.idx = idx

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
