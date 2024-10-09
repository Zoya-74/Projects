"""Inheritance Example: Companies and Employees
=== CSC148 Winter 2022 ===
Department of Mathematical and Computational Sciences,
University of Toronto Mississauga
=== Module Description ===
This module contains an illustration of *inheritance* through an abstract
Employee class that defines a common interface for all of its subclasses.
In this second version, we:
- add attributes and initializers, and use the attributes instead of hard-coded
values
- illustrate the benefit of inheritance in the simple Company class,
which stores different types of employees.
"""
from datetime import date


class Employee:
    """An employee of a company.
    This is an abstract class. Only subclasses should be instantiated.
    === Attributes ===
    id_: This employee's ID number.
    name: This employee's name.
    """
    id_: int
    name: str

    def __init__(self, id_: int, name: str) -> None:
        """Initialize this employee.
        Note: This initializer is meant for internal use only;
        Employee is an abstract class and should not be instantiated directly.
        """
        self.id_ = id_
        self.name = name

    def get_monthly_payment(self) -> float:
        """Return the amount that this Employee should be paid in one month.
        Round the amount to the nearest cent.
        """
        raise NotImplementedError

    def pay(self, pay_date: date) -> None:
        """Pay this Employee on the given date and record the payment.
        (Assume this is called once per month.)
        """
        payment = self.get_monthly_payment()
        print(f'An employee was paid {payment} on {pay_date}.')


class SalariedEmployee(Employee):
    """An employee whose pay is computed based on an annual salary.
    === Attributes ===
    salary: This employee's annual salary
    === Representation invariants ===
    - salary >= 0
    """
    id_: int
    name: str
    salary: float

    def __init__(self, id_: int, name: str, salary: float) -> None:
        """Initialize this salaried Employee.
        >>> e = SalariedEmployee(14, 'Fred Flintstone', 5200.0)
        >>> e.salary
        5200.0
        """
        # Note that to call the superclass initializer, we need to use the
        # full method name '__init__'. This is the only time you should write
        # '__init__' explicitly.
        Employee.__init__(self, id_, name)
        self.salary = salary

    def get_monthly_payment(self) -> float:
        """Return the amount that this Employee should be paid in one month.
        Round the amount to the nearest cent.
        >>> e = SalariedEmployee(99, 'Mr Slate', 120000.0)
        >>> e.get_monthly_payment()
        10000.0
        """
        return round(self.salary / 12, 2)


class HourlyEmployee(Employee):
    """An employee whose pay is computed based on an hourly rate.
    === Attributes ===
    hourly_wage:
    This employee's hourly rate of pay.
    hours_per_month:
    The number of hours this employee works each month.
    === Representation invariants ===
    - hourly_wage >= 0
    - hours_per_month >= 0
    """
    id_: int
    name: str
    hourly_wage: float
    hours_per_month: float

    def __init__(self, id_: int, name: str, hourly_wage: float,
                 hours_per_month: float) -> None:
        """Initialize this HourlyEmployee.
        >>> barney = HourlyEmployee(23, 'Barney Rubble', 1.25, 50.0)
        >>> barney.hourly_wage
        1.25
        >>> barney.hours_per_month
        50.0
        """
        Employee.__init__(self, id_, name)
        self.hourly_wage = hourly_wage
        self.hours_per_month = hours_per_month

    def get_monthly_payment(self) -> float:
        """Return the amount that this Employee should be paid in one month.
        Round the amount to the nearest cent.
        >>> e = HourlyEmployee(23, 'Barney Rubble', 1.25, 50)
        >>> e.get_monthly_payment()
        62.5
        """
        return self.hours_per_month * self.hourly_wage


class Company:
    """A company with employees.
    We use this class mainly as a client for the various Employee classes
    we defined in employee.
    === Public Attributes ===
    employees: the employees in the company.
    """
    employees: list[Employee]

    def __init__(self, employees: list[Employee]) -> None:
        self.employees = employees

    def pay_all(self, pay_date: date) -> None:
        """Pay all employees at this company."""

        for employee in self.employees:
            employee.pay(pay_date)


if __name__ == '__main__':
    # import python_ta
    # python_ta.check_all()
    # Illustrate a small company.
    my_corp = Company([SalariedEmployee(14, 'Fred Flintstone', 5200.0),
                       HourlyEmployee(23, 'Barney Rubble', 1.25, 50.0),
                       SalariedEmployee(99, 'Mr Slate', 120000.0)])
    my_corp.pay_all(date(2017, 8, 31))
    my_corp.pay_all(date(2017, 9, 30))
