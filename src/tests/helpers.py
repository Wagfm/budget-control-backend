import datetime as dt
import random
import string


class FakeDataGenerator:
    def __init__(self) -> None:
        pass

    @staticmethod
    def string(length: int) -> str:
        return str.join("", random.choices(string.ascii_uppercase + string.ascii_lowercase, k=length))

    @staticmethod
    def date() -> dt.date:
        year = random.randint(1900, 2100)
        month = random.randint(1, 12)
        if month == 2:
            if year % 4 == 0 and year % 100 != 0:
                return dt.date(year, month, random.randint(1, 29))
            return dt.date(year, month, random.randint(1, 28))
        if month in [1, 3, 5, 7, 8, 10, 12]:
            return dt.date(year, month, random.randint(1, 31))
        return dt.date(year=year, month=month, day=random.randint(1, 30))

    @staticmethod
    def float() -> float:
        return random.random() * random.randint(1, 1_000)
