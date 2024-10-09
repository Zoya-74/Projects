"""
CSC148, Winter 2024
Assignment 1

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2022 Bogdan Simion, Diane Horton, Jacqueline Smith
"""
import datetime
from math import ceil
from typing import Optional
from bill import Bill
from call import Call

# Constants for the month-to-month contract monthly fee and term deposit
MTM_MONTHLY_FEE = 50.00
TERM_MONTHLY_FEE = 20.00
TERM_DEPOSIT = 300.00

# Constants for the included minutes and SMSs in the term contracts (per month)
TERM_MINS = 100

# Cost per minute and per SMS in the month-to-month contract
MTM_MINS_COST = 0.05

# Cost per minute and per SMS in the term contract
TERM_MINS_COST = 0.1

# Cost per minute and per SMS in the prepaid contract
PREPAID_MINS_COST = 0.025


class Contract:
    """ A contract for a phone line

    This class is not to be changed or instantiated. It is an Abstract Class.

    === Public Attributes ===
    start:
         starting date for the contract
    bill:
         bill for this contract for the last month of call records loaded from
         the input dataset
    """
    start: datetime.date
    bill: Optional[Bill]

    def __init__(self, start: datetime.date) -> None:
        """ Create a new Contract with the <start> date, starts as inactive
        """
        self.start = start
        self.bill = None

    def new_month(self, month: int, year: int, bill: Bill) -> None:
        """ A new month has begun corresponding to <month> and <year>.
        This may be the first month of the contract.
        Store the <bill> argument in this contract and set the appropriate rate
        per minute and fixed cost.

        DO NOT CHANGE THIS METHOD
        """
        raise NotImplementedError

    def bill_call(self, call: Call) -> None:
        """ Add the <call> to the bill.

        Precondition:
        - a bill has already been created for the month+year when the <call>
        was made. In other words, you can safely assume that self.bill has been
        already advanced to the right month+year.
        """
        self.bill.add_billed_minutes(ceil(call.duration / 60.0))

    def cancel_contract(self) -> float:
        """ Return the amount owed in order to close the phone line associated
        with this contract.

        Precondition:
        - a bill has already been created for the month+year when this contract
        is being cancelled. In other words, you can safely assume that self.bill
        exists for the right month+year when the cancelation is requested.
        """
        self.start = None
        return self.bill.get_cost()


class TermContract(Contract):
    """A term contract for a phone line
    This class is for phone lines with a start and end date
    === Public Attributes ===
    start:
        the date of the beginning of the contract
    end:
        the date the term contract ends
    bill:
         bill for this contract for the last month of call records loaded from
         the input dataset
        """
    # === Private Attributes ===
    # _date_tracker:
    #    A date that is updated each month to reflect the current date of the
    #    contract
    # _term_deposit:
    #    The initial deposit amount the customer pays at the beginning of
    #    the contract
    # _term_monthly_fee:
    #    The monthly fee billed each month to the customer in the term contract
    # _free_min_track:
    #    The remaining free minutes the customer has available for use

    start: datetime.date
    end: datetime.date
    bill: Optional[Bill]
    _date_tracker: datetime.date
    _term_deposit: float
    _term_monthly_fee: float
    _free_min_track: float

    def __init__(self, start: datetime.date, end: datetime.date) -> None:
        """ Create a new Contract with the <start> date, starts as inactive
        """
        self.end = end
        Contract.__init__(self, start)
        self._date_tracker = start
        self._free_min_track = 100
        self._term_deposit = TERM_DEPOSIT
        self._term_monthly_fee = TERM_MONTHLY_FEE

    def new_month(self, month: int, year: int, bill: Bill) -> None:
        """ A new month has begun corresponding to <month> and <year>.
        This may be the first month of the contract.
        Store the <bill> argument in this contract and set the appropriate rate
        per minute and fixed cost.
        """
        # configure the bill to have term contract with the appropriate rates
        bill.set_rates("TERM", TERM_MINS_COST)
        self._free_min_track = 100

        # If this is the first month, customer must pay a term deposit in bill
        if month == self.start.month and year == self.start.year:
            bill.add_fixed_cost(self._term_deposit)

        # A monthly fee also added to bill
        bill.add_fixed_cost(self._term_monthly_fee)

        # Assign the current bill to the contract class
        self.bill = bill
        # Update the date tracker, so we can check if cancellation is after or
        # before end date
        self._date_tracker = datetime.date(year, month, 1)

    def bill_call(self, call: Call) -> None:
        """ Add the <call> to the bill. If customer has free minutes for this
        month, the remaining minutes of the call will be added to the bill

        Precondition:
        - a bill has already been created for the month+year when the <call>
        was made. In other words, you can safely assume that self.bill has been
        already advanced to the right month+year.
        """
        billed = ceil(call.duration / 60.0)

        # If the duration is under how many minutes the customer has for that
        # month, don't charge the customer, and update free minutes since they
        # use them in this call
        if billed <= self._free_min_track != 0:
            # Update bill for how many free minute customer **used**
            self.bill.add_free_minutes(billed)

            # Update my tracker of how many free minutes customer has **left**
            self._free_min_track -= billed
        else:
            # If the duration is more than the free minutes customer
            # has left, charge them with the remaining minutes
            self.bill.add_billed_minutes(int(billed - self._free_min_track))

            # Customer has used up all their remaining free minutes, so update
            # bill to indicate
            self.bill.add_free_minutes(int(self._free_min_track))

            # Since all free minutes are used, update my tracker
            self._free_min_track = 0

    def cancel_contract(self) -> float:
        """ Return the amount owed in order to close the phone line associated
        with this contract. If cancelled on or after end date of contract, term
        deposit will be returned

        Precondition:
        - a bill has already been created for the month+year when this contract
        is being cancelled. In other words, you can safely assume that self.bill
        exists for the right month+year when the cancelation is requested.
        """
        self.start = None

        # If customer cancels after end date of contract, they will receive
        # their term deposit back. So the amount they owe will be less by a
        # factor of the term deposit
        if self._date_tracker >= self.end:
            self.bill.add_fixed_cost(-1 * self._term_deposit)

        return self.bill.get_cost()


class MTMContract(Contract):
    """A Month-to-Month contract for a phone line
    This class is for phone lines with a start date and no other commitments
    === Public Attributes ===
    start:
        the date of the beginning of the contract
    bill:
         bill for this contract for the last month of call records loaded from
         the input dataset
        """
    start: datetime.date
    bill: Optional[Bill]

    # MTM contract has no extra attributes, thus no initializer is required
    def new_month(self, month: int, year: int, bill: Bill) -> None:
        """ A new month has begun corresponding to <month> and <year>.
        This may be the first month of the contract.
        Store the <bill> argument in this contract and set the appropriate rate
        per minute and fixed cost.
        """
        # Simply configure the bill and store it in bill attribute since
        # it's the most recent bill
        bill.set_rates("MTM", MTM_MINS_COST)
        bill.add_fixed_cost(MTM_MONTHLY_FEE)
        self.bill = bill
    # The other methods are the same as parent class, thus no need to write


class PrepaidContract(Contract):
    """
    A contract with a start date and an account balance that is the amount
    of money the customer owes / how much credit is available.
    == Public Attributes ==
    start:
        the date of the beginning of the contract
    balance:
        the amount of money the customer owes. If negative, then customer
        has <balance> amount of credit.
    bill:
         bill for this contract for the last month of call records loaded from
         the input dataset
    """
    start: datetime.date
    bill: Optional[Bill]
    balance: float

    def __init__(self, start: datetime.date, balance: float) -> None:
        Contract.__init__(self, start)
        self.balance = -1 * balance

    def new_month(self, month: int, year: int, bill: Bill) -> None:
        """ A new month has begun corresponding to <month> and <year>.
        This may be the first month of the contract.
        Store the <bill> argument in this contract and set the appropriate rate
        per minute and fixed cost. The balance of the previous month will be
        carried over to the new month
        """
        # Assign current bill to the contract since it is the most recent one

        self.bill = bill

        # Add the credit or amount owed to this bill. This is the carry over
        # from last month
        self.bill.add_fixed_cost(self.balance)

        # Add a top-up and charge to bill appropriately
        if self.balance > -10:
            self.balance -= 25
            self.bill.add_fixed_cost(-25)

        self.bill.set_rates("PREPAID", PREPAID_MINS_COST)

        # The new balance will be the cost of the bill
        self.balance = self.bill.get_cost()

    def bill_call(self, call: Call) -> None:
        """ Add the <call> to the bill.

        Precondition:
        - a bill has already been created for the month+year when the <call>
        was made. In other words, you can safely assume that self.bill has been
        already advanced to the right month+year.
        """
        billed = ceil(call.duration / 60.0)
        call_cost = billed * PREPAID_MINS_COST

        # Update balance with the cost of the call, and bill it to the bill
        self.balance += call_cost
        self.bill.add_billed_minutes(ceil(call.duration / 60.0))

    def cancel_contract(self) -> float:
        """ Return the amount owed in order to close the phone line associated
        with this contract.

        Precondition:
        - a bill has already been created for the month+year when this contract
        is being cancelled. In other words, you can safely assume that self.bill
        exists for the right month+year when the cancellation is requested.
        """
        # If customer has credit, they will not get it back once cancelling
        # contract, only the amount owed is returned
        if self.bill.get_cost() < 0:
            return 0

        return self.bill.get_cost()


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'allowed-import-modules': [
            'python_ta', 'typing', 'datetime', 'bill', 'call', 'math'
        ],
        'disable': ['R0902', 'R0913'],
        'generated-members': 'pygame.*'
    })
