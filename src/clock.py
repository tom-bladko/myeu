from datetime import date, datetime

YEAR_START = 1200
YEAR_END = 1925

class Clock:

    def __init__(self, year=1400, month=1, date_str=None):
        if date_str:
            self.convert_from_str(date_str)
        else:
            self.current_year = year
            self.current_month = month
        self.events = []

    #
    #   SEASON
    #

    def get_season(self):
        if self.current_month in [1, 2, 3]:
            return "Winter"
        elif self.current_month in [4, 5, 6]:
            return "Spring"
        elif self.current_month in [7, 8, 9]:
            return "Summer"
        elif self.current_month in [10, 11, 12]:
            return "Fall"

    @property
    def season(self):
        return self.get_season()

    #
    #   OPERATIONS
    #

    def add_months(self, months):
        total_months = self.current_month + months
        self.current_year += (total_months - 1) // 12
        self.current_month = (total_months - 1) % 12 + 1

    def subtract_months(self, months):
        total_months = (self.current_year * 12 + self.current_month - 1) - months
        self.current_year = total_months // 12
        self.current_month = total_months % 12 + 1

    def add_years(self, years):
        self.current_year += years

    def subtract_years(self, years):
        self.current_year -= years

    #
    #   TURNS
    #

    def calculate_turns_from_start(self):
        total_months_start = YEAR_START * 12 + 1
        total_months_current = self.current_year * 12 + self.current_month
        return total_months_current - total_months_start

    def calculate_turns_from_date(self, year, month):
        total_months_start = YEAR_START * 12 + 1
        total_months_target = year * 12 + month
        return total_months_target - total_months_start

    def calculate_turns_to_date(self, year, month):
        total_months_start = YEAR_END * 12 + 1
        total_months_target = year * 12 + month
        return total_months_target - total_months_start

    def calculate_turns_until_end(self):
        total_months_end = YEAR_END * 12 + 12
        total_months_current = self.current_year * 12 + self.current_month
        return total_months_end - total_months_current

    #
    #   ROUND
    #

    def round_to_closest_month(self, date_str):
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        if date_obj.day > 15:
            date_obj = date_obj.replace(day=1)
        else:
            date_obj = date_obj.replace(day=1)
        self.current_year = date_obj.year
        self.current_month = date_obj.month
        self.add_months(1)

    def round_to_beginning_of_year(self):
        self.current_month = 1

    def round_to_closest_decade(self):
        if self.current_year % 10 >= 5:
            self.current_year = (self.current_year // 10 + 1) * 10
        else:
            self.current_year = (self.current_year // 10) * 10

    #
    #   PRINT
    #

    def __str__(self):
        import calendar
        month_abbr = calendar.month_abbr[self.current_month]
        return f"{self.current_year:04d}-{month_abbr}"

    #
    #   CHECK RANGE
    #

    def difference_in_years(self, other_clock):
        years_diff = other_clock.current_year - self.current_year
        if other_clock.current_month < self.current_month:
            years_diff -= 1
        return years_diff

    def difference_in_months(self, other_clock):
        total_months_current = self.current_year * 12 + self.current_month
        total_months_other = other_clock.current_year * 12 + other_clock.current_month
        return total_months_other - total_months_current

    def difference_in_days(self, other_clock):
        total_days_current = (self.current_year * 12 + self.current_month) * 30
        total_days_other = (other_clock.current_year * 12 + other_clock.current_month) * 30
        return total_days_other - total_days_current

    def is_within_range(self, months_difference):
        current_total_months = self.current_year * 12 + self.current_month
        target_total_months = current_total_months + months_difference
        return target_total_months >= 0

    #
    #   CONVERT FROM DATE
    #

    def convert_to_str(self):
        return f"{self.current_year:04d}-{self.current_month:02d}-01"

    def convert_from_str(self, date_str):
        year, month, _ = map(int, date_str.split('-'))
        self.current_year = year
        self.current_month = month

    def load_from_date(self, date_obj):
        self.current_year = date_obj.year
        self.current_month = date_obj.month

    def save_to_date(self):
        return date(self.current_year, self.current_month, 1)

    #
    #   OPERATORS
    #

    def __add__(self, other):
        if not isinstance(other, Clock):
            return NotImplemented
        total_months = self.current_year * 12 + self.current_month + other.current_year * 12 + other.current_month
        new_year = total_months // 12
        new_month = total_months % 12
        return Clock(new_year, new_month)

    def __sub__(self, other):
        if not isinstance(other, Clock):
            return NotImplemented
        total_months = self.current_year * 12 + self.current_month - (other.current_year * 12 + other.current_month)
        new_year = total_months // 12
        new_month = total_months % 12
        return Clock(new_year, new_month)

    #
    #   EVENT
    #

    def schedule_event(self, event_date, callback):
        self.events.append((event_date, callback))
        self.events.sort()

    def check_events(self):
        current_date = self.convert_to_str()
        for event_date, callback in self.events:
            if event_date <= current_date:
                callback()
                self.events.remove((event_date, callback))


toml_data = """
data = 10
date = 2014-10-10
"""

import toml

parsed_toml_data = toml.loads(toml_data)
print(parsed_toml_data)
a = Clock(date_str = '1792-09-10')
print( a )
c = Clock(1400, 10)
b = Clock( 1450, 3)
d = c - b
c.add_months( 50 )
print( d )
print( c.convert_to_str() )