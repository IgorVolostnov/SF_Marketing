import calendar
from datetime import datetime
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

    def amount_work_days_month(self, current_month: int) -> int:
        last_day = calendar.monthrange(2025, current_month)[1]
        days = (datetime(2025, current_month, x) for x in range(1, last_day + 1))
        days = map(lambda day: self.is_working_day(day), days)
        work_days = sum(days)
        return work_days

    def prepayment(self, salary_amount: int, current_month: int, work_days: int) -> int:
        last_day = calendar.monthrange(2025, current_month)[1]
        days = (datetime(2025, current_month, x) for x in range(1, last_day + 1))
        days = map(lambda day: self.is_working_day(day), days)
        all_work_days = sum(days)
        money_one_day = salary_amount / all_work_days
        prepayment_days = (datetime(2025, current_month, x) for x in range(1, 16))
        prepayment_days = map(lambda day: self.is_working_day(day), prepayment_days)
        prepayment_work_days = sum(prepayment_days)
        if work_days <= prepayment_work_days:
            total = 0
        else:
            total = money_one_day * prepayment_work_days
        return round(total)

    def salary(self, salary_amount: int, current_month: int, work_days: int) -> int:
        last_day = calendar.monthrange(2025, current_month)[1]
        days = (datetime(2025, current_month, x) for x in range(1, last_day + 1))
        days = map(lambda day: self.is_working_day(day), days)
        all_work_days = sum(days)
        money_one_day = salary_amount / all_work_days
        prepayment_days = (datetime(2025, current_month, x) for x in range(1, 16))
        prepayment_days = map(lambda day: self.is_working_day(day), prepayment_days)
        prepayment_work_days = sum(prepayment_days)
        salary_days = (datetime(2025, current_month, x) for x in range(16, last_day + 1))
        salary_days = map(lambda day: self.is_working_day(day), salary_days)
        salary_work_days = sum(salary_days)
        if work_days <= prepayment_work_days:
            total = money_one_day * work_days
        else:
            if work_days < all_work_days:
                total = money_one_day * (work_days - prepayment_work_days)
            else:
                total = money_one_day * salary_work_days
        return round(total)

    @staticmethod
    def award(money_turnover: int, gross_profit: int) -> int:
        if gross_profit == 0:
            total = 0
        else:
            profitability = gross_profit / money_turnover
            if money_turnover <= 1000000:
                total = 0
            elif 1000000 < money_turnover <= 5000000:
                total = gross_profit * 0.05
            elif 5000000 < money_turnover <= 10000000:
                total = 5000000 * profitability * 0.05 + (money_turnover - 5000000) * profitability * 0.04
            else:
                total = 5000000 * profitability * 0.05 + 5000000 * profitability * 0.04 + (
                            money_turnover - 10000000) * profitability * 0.03
        return round(total)
