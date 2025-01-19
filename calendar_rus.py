from workalendar.europe import Russia
from workalendar.registry_tools import iso_register


@iso_register('RU')
class Rus(Russia):
    FIXED_HOLIDAYS = (
        (1, 1, "New year"),
        (1, 2, "Day After New Year"),
        (1, 3, "Third Day after New Year"),
        (1, 4, "Fourth Day after New Year"),
        (1, 5, "Fifth Day after New Year"),
        (1, 6, "Sixth Day after New Year"),
        (1, 7, "Christmas"),
        (5, 1, "The Day of Spring and Labour"),
        (5, 2, "The Day of Spring and Labour shift"),
        (5, 8, "Before Victory Day"),
        (5, 9, "Victory Day"),
        (6, 12, "National Day"),
        (6, 13, "National Day shift"),
        (11, 4, "Day of Unity"),
        (12, 31, "Before New year"),
    )

    def get_variable_days(self, year):
        # usual variable days
        days = super().get_variable_days(year)
        return days
