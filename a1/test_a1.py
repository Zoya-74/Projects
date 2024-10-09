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

import bill
import pytest

from application import create_customers, process_event_history, \
    find_customer_by_number
# from contract import TermContract, MTMContract, PrepaidContract
from customer import Customer
from filter import DurationFilter, CustomerFilter, ResetFilter
from phoneline import PhoneLine
from callhistory import CallHistory
from call import Call
from contract import TermContract, PrepaidContract, MTMContract
from bill import Bill

"""
This is a sample test file with a limited set of cases, which are similar in
nature to the full autotesting suite

Use this framework to check some of your work and as a starting point for
creating your own tests

*** Passing these tests does not mean that it will necessarily pass the
autotests ***
"""


def create_single_customer_with_all_lines() -> Customer:
    """ Create a customer with one of each type of PhoneLine
    """
    contracts = [
        TermContract(start=datetime.date(year=2017, month=12, day=25),
                     end=datetime.date(year=2019, month=6, day=25)),
        MTMContract(start=datetime.date(year=2017, month=12, day=25)),
        PrepaidContract(start=datetime.date(year=2017, month=12, day=25),
                        balance=100)
    ]
    numbers = ['867-5309', '273-8255', '649-2568']
    customer = Customer(cid=7777)

    for i in range(len(contracts)):
        customer.add_phone_line(PhoneLine(numbers[i], contracts[i]))

    customer.new_month(12, 2017)
    return customer


test_dict = {'events': [
    {"type": "sms",
     "src_number": "867-5309",
     "dst_number": "273-8255",
     "time": "2018-01-01 01:01:01",
     "src_loc": [-79.42848154284123, 43.641401675960374],
     "dst_loc": [-79.52745693913239, 43.750338501653374]},
    {"type": "sms",
     "src_number": "273-8255",
     "dst_number": "649-2568",
     "time": "2018-01-01 01:01:02",
     "src_loc": [-79.42848154284123, 43.641401675960374],
     "dst_loc": [-79.52745693913239, 43.750338501653374]},
    {"type": "sms",
     "src_number": "649-2568",
     "dst_number": "867-5309",
     "time": "2018-01-01 01:01:03",
     "src_loc": [-79.42848154284123, 43.641401675960374],
     "dst_loc": [-79.52745693913239, 43.750338501653374]},
    {"type": "call",
     "src_number": "273-8255",
     "dst_number": "867-5309",
     "time": "2018-01-01 01:01:04",
     "duration": 10,
     "src_loc": [-79.42848154284123, 43.641401675960374],
     "dst_loc": [-79.52745693913239, 43.750338501653374]},
    {"type": "call",
     "src_number": "867-5309",
     "dst_number": "649-2568",
     "time": "2018-01-01 01:01:05",
     "duration": 50,
     "src_loc": [-79.42848154284123, 43.641401675960374],
     "dst_loc": [-79.52745693913239, 43.750338501653374]},
    {"type": "call",
     "src_number": "649-2568",
     "dst_number": "273-8255",
     "time": "2018-01-01 01:01:06",
     "duration": 50,
     "src_loc": [-79.42848154284123, 43.641401675960374],
     "dst_loc": [-79.52745693913239, 43.750338501653374]}
],
    'customers': [
        {'lines': [
            {'number': '867-5309',
             'contract': 'term'},
            {'number': '273-8255',
             'contract': 'mtm'},
            {'number': '649-2568',
             'contract': 'prepaid'}
        ],
            'id': 7777},
        {'lines': [
            {'number': '647-5646',
             'contract': 'prepaid'}
        ],
            'id': 1900}
    ]
}


def test_process_event_history() -> None:
    """tests to see if the function process event history is working properly"""
    customers = create_customers(test_dict)
    process_event_history(test_dict, customers)
    assert len(
        find_customer_by_number('273-8255', customers).get_history()) == 2


def test_cancel_term_contract() -> None:
    """tests to see if the cancellation of the term contract class was coded
    as intended."""
    time2 = "2019-06-01 01:01:05"
    curr_date = datetime.datetime.strptime(time2,
                                           "%Y-%m-%d %H:%M:%S")
    caller_num = "867-5309"
    callee_num = "273-8255"
    call_date = curr_date
    call_duration = 3000
    caller_loc = (-79.42848154284123, 43.641401675960374)
    callee_loc = (-79.52745693913239, 43.750338501653374)

    call = Call(caller_num, callee_num, call_date,
                call_duration, caller_loc, callee_loc)

    start_date = datetime.date(2019, 1, 1)
    end_date = datetime.date(2020, 1, 1)
    current_date = datetime.date(2019, 6, 1)
    c1 = TermContract(start_date, end_date)
    c1.bill = Bill()
    c1.bill.type = TermContract
    c1.bill.add_fixed_cost(20.00)
    c1.bill_call(call)
    c1.bill.add_fixed_cost(300.00)
    c1.bill.set_rates('term', 0.1)
    c1._recent_month = (current_date.month, current_date.year)
    cancel_amount = c1.cancel_contract()
    actual_amount = (20.00 + 300.00)
    assert c1.bill.free_min == 50
    assert c1.start is None
    assert cancel_amount == actual_amount


def test_out_going_and_incoming_calls() -> None:
    """Tests to see if the function register outgoing calls and register
    incoming calls is working as intended."""
    test_events_inside = [
        {"type": "call", "src_number": "867-5309", "dst_number":
            "273-8255", "time": "2018-01-01 01:01:04", "duration": 50,
         "src_loc": [-79.42848154284123, 43.641401675960374],
         "dst_loc": [-79.52745693913239, 43.750338501653374]},
        {"type": "call", "src_number": "867-5309", "dst_number":
            "649-2568", "time": "2018-02-01 01:01:05", "duration": 60,
         "src_loc": [-79.42848154284123, 43.641401675960374],
         "dst_loc": [-79.52745693913239, 43.750338501653374]}
    ]

    call_history = CallHistory()

    # Process each call event
    for event in test_events_inside:
        curr_date = datetime.datetime.strptime(event['time'],
                                               "%Y-%m-%d %H:%M:%S")
        caller_num = event["src_number"]
        callee_num = event["dst_number"]
        call_date = curr_date
        call_duration = int(event["duration"])
        caller_loc = tuple(event["src_loc"])
        callee_loc = tuple(event["dst_loc"])

        call = Call(caller_num, callee_num, call_date,
                    call_duration, caller_loc, callee_loc)

        call_history.register_outgoing_call(call)

    # Assertions
    assert (1, 2018) in call_history.outgoing_calls
    assert (2, 2018) in call_history.outgoing_calls
    assert len(call_history.outgoing_calls[(1, 2018)]) == 1
    assert len(call_history.outgoing_calls[(2, 2018)]) == 1
    assert call_history.outgoing_calls[(1, 2018)][0].src_number == "867-5309"
    assert call_history.outgoing_calls[(2, 2018)][0].src_number == "867-5309"


def test_customer_creation() -> None:
    """ Test for the correct creation of Customer, PhoneLine, and Contract
    classes
    """
    customer = create_single_customer_with_all_lines()
    billi = customer.generate_bill(12, 2017)

    assert len(customer.get_phone_numbers()) == 3
    assert len(billi) == 3
    assert billi[0] == 7777
    assert billi[1] == 270.0
    assert len(billi[2]) == 3
    assert billi[2][0]['total'] == 320
    assert billi[2][1]['total'] == 50
    assert billi[2][2]['total'] == -100

    # Check for the customer creation in application.py
    customer = create_customers(test_dict)[0]
    customer.new_month(12, 2017)
    bill = customer.generate_bill(12, 2017)

    assert len(customer.get_phone_numbers()) == 3
    assert len(bill) == 3
    assert bill[0] == 7777
    assert bill[1] == 270.0
    assert len(bill[2]) == 3
    assert bill[2][0]['total'] == 320
    assert bill[2][1]['total'] == 50
    assert bill[2][2]['total'] == -100


test_dict2 = {'events': [
    {"type": "call",
     "src_number": "649-2568",
     "dst_number": "647-5646",
     "time": "2018-01-01 01:01:06",
     "duration": 50,
     "src_loc": [-79.42848154284123, 43.641401675960374],
     "dst_loc": [-79.52745693913239, 43.750338501653374]}
],
    'customers': [
        {'lines': [
            {'number': '649-2568',
             'contract': 'prepaid'}
        ],
            'id': 7777},
        {'lines': [
            {'number': '647-5646',
             'contract': 'prepaid'}
        ],
            'id': 1900}
    ]
}


def test_prepaid_contract_simple() -> None:
    """tests the prepaid contract."""
    customers = create_customers(test_dict2)
    customers[0].new_month(1, 2018)

    process_event_history(test_dict2, customers)

    bill2 = customers[0].generate_bill(1, 2018)
    assert bill2[1] == -99.975


def test_events() -> None:
    """ Test the ability to make calls, and ensure that the CallHistory objects
    are populated
    """
    customers = create_customers(test_dict)
    customers[0].new_month(1, 2018)

    process_event_history(test_dict, customers)

    # Check the bill has been computed correctly
    bill = customers[0].generate_bill(1, 2018)
    assert bill[2][0]['free_mins'] == 1
    assert bill[0] == 7777
    assert bill[1] == pytest.approx(-29.925)
    assert bill[2][0]['total'] == pytest.approx(20)
    assert bill[2][1]['total'] == pytest.approx(50.05)
    assert bill[2][1]['billed_mins'] == 1
    assert bill[2][2]['total'] == pytest.approx(-99.975)
    assert bill[2][2]['billed_mins'] == 1

    # Check the CallHistory objects are populated
    history = customers[0].get_call_history('867-5309')
    assert len(history) == 1
    assert len(history[0].incoming_calls) == 1
    assert len(history[0].outgoing_calls) == 1

    history = customers[0].get_call_history()
    assert len(history) == 3
    assert len(history[0].incoming_calls) == 1
    assert len(history[0].outgoing_calls) == 1


def test_contract_start_dates() -> None:
    """ Test the start dates of the contracts.

    Ensure that the start dates are the correct dates as specified in the given
    starter code.
    """
    customers = create_customers(test_dict)
    for c in customers:
        for pl in c._phone_lines:
            assert pl.contract.start == datetime.date(
                year=2017, month=12, day=25)
            if hasattr(pl.contract,
                       'end'):  #only check if there is an end date(TermContract)
                assert pl.contract.end == datetime.date(
                    year=2019, month=6, day=25)


def test_filters() -> None:
    """ Test the functionality of the filters.

    We are only giving you a couple of tests here, you should expand both the
    dataset and the tests for the different types of applicable filters
    """
    customers = create_customers(test_dict)
    process_event_history(test_dict, customers)

    # Populate the list of calls:
    calls = []
    hist = customers[0].get_history()
    # only consider outgoing calls, we don't want to duplicate calls in the test
    calls.extend(hist[0])

    # The different filters we are testing
    filters = [
        DurationFilter(),
        CustomerFilter(),
        ResetFilter()
    ]

    # These are the inputs to each of the above filters in order.
    # Each list is a test for this input to the filter
    filter_strings = [
        ["L050", "G010", "L000", "50", "AA", ""],
        ["7777", "1111", "9999", "aaaaaaaa", ""],
        ["rrrr", ""]
    ]

    # These are the expected outputs from the above filter application
    # onto the full list of calls
    expected_return_lengths = [
        [1, 2, 0, 3, 3, 3],
        [3, 3, 3, 3, 3],
        [3, 3]
    ]

    for i in range(len(filters)):
        for j in range(len(filter_strings[i])):
            result = filters[i].apply(customers, calls, filter_strings[i][j])
            assert len(result) == expected_return_lengths[i][j]


test_dict_1 = {'events': [],
               'customers': []}


def test_process_empty_1() -> None:
    assert process_event_history(test_dict_1, []) is None


test_dict_2 = {'events': [
    {"type": "call",
     "src_number": "386-6346",
     "dst_number": "131-3768",
     "time": "2018-01-01 01:01:01",
     "duration": 60,
     "src_loc": [-79.42848154284123, 43.641401675960374],
     "dst_loc": [-79.52745693913239, 43.750338501653374]},
    {"type": "call",
     "src_number": "386-6346",
     "dst_number": "934-0592",
     "time": "2018-01-01 01:01:04",
     "duration": 60,
     "src_loc": [-79.42848154284123, 43.641401675960374],
     "dst_loc": [-79.52745693913239, 43.750338501653374]},
    {"type": "call",
     "src_number": "386-6346",
     "dst_number": "123-4567",
     "time": "2018-01-01 01:01:05",
     "duration": 60,
     "src_loc": [-79.42848154284123, 43.641401675960374],
     "dst_loc": [-79.52745693913239, 43.750338501653374]},
    {"type": "call",
     "src_number": "386-6346",
     "dst_number": "426-4804",
     "time": "2018-01-01 01:01:06",
     "duration": 60,
     "src_loc": [-79.42848154284123, 43.641401675960374],
     "dst_loc": [-79.52745693913239, 43.750338501653374]},
    {"type": "call",
     "src_number": "131-3768",
     "dst_number": "426-4804",
     "time": "2018-02-01 01:01:06",
     "duration": 18000,
     "src_loc": [-79.42848154284123, 43.641401675960374],
     "dst_loc": [-79.52745693913239, 43.750338501653374]}
],
    "customers": [
        {"lines": [{"number": "123-4567", "contract": "mtm"}], "id": 2247},
        {"lines": [{"number": "426-4804", "contract": "term"},
                   {"number": "934-0592", "contract": "term"},
                   {"number": "131-3768", "contract": "prepaid"},
                   {"number": "386-6346", "contract": "term"}], "id": 3895},
    ]
}

test_dict_10 = {'events': [
    {"type": "call",
     "src_number": "123-4567",
     "dst_number": "131-3768",
     "time": "2018-01-01 01:01:01",
     "duration": 20,
     "src_loc": [-79.42848154284123, 43.641401675960374],
     "dst_loc": [-79.52745693913239, 43.750338501653374]},
    {"type": "call",
     "src_number": "386-6346",
     "dst_number": "934-0592",
     "time": "2018-01-01 01:01:04",
     "duration": 10,
     "src_loc": [-79.42848154284123, 43.641401675960374],
     "dst_loc": [-79.52745693913239, 43.750338501653374]},
    {"type": "call",
     "src_number": "131-3768",
     "dst_number": "123-4567",
     "time": "2018-01-01 01:01:05",
     "duration": 50,
     "src_loc": [-79.42848154284123, 43.641401675960374],
     "dst_loc": [-79.52745693913239, 43.750338501653374]},
    {"type": "call",
     "src_number": "934-0592",
     "dst_number": "426-4804",
     "time": "2018-01-01 01:01:06",
     "duration": 50,
     "src_loc": [-79.42848154284123, 43.641401675960374],
     "dst_loc": [-79.52745693913239, 43.750338501653374]},
    {"type": "call",
     "src_number": "934-0592",
     "dst_number": "426-4804",
     "time": "2018-02-01 01:01:06",
     "duration": 50,
     "src_loc": [-79.42848154284123, 43.641401675960374],
     "dst_loc": [-79.52745693913239, 43.750338501653374]}
],
    "customers": [
        {"lines": [{"number": "123-4567", "contract": "mtm"}], "id": 2247},
        {"lines": [{"number": "426-4804", "contract": "term"},
                   {"number": "934-0592", "contract": "term"},
                   {"number": "131-3768", "contract": "prepaid"},
                   {"number": "386-6346", "contract": "term"}], "id": 3895},
    ]
}


def test_bill_created_for_new_month_when_not_called_on_contract() -> None:
    customers = create_customers_2(test_dict_10)
    process_event_history(test_dict_10, customers)
    billi = customers[0].generate_bill(2, 2018)
    assert billi[0] == 2247
    assert billi[1] == 50


def test_process_term() -> None:
    customers = create_customers_2(test_dict_2)
    process_event_history(test_dict_2, customers)
    billi = customers[1].generate_bill(2, 2018)
    assert billi[1] == -40 + 7.5


test_dict_3 = {'events': [
    {"type": "call",
     "src_number": "123-4567",
     "dst_number": "426-4804",
     "time": "2018-01-01 01:01:04",
     "duration": 10,
     "src_loc": [-79.42848154284123, 43.641401675960374],
     "dst_loc": [-79.52745693913239, 43.750338501653374]},
    {"type": "call",
     "src_number": "123-4567",
     "dst_number": "426-4805",
     "time": "2018-01-01 01:01:05",
     "duration": 50,
     "src_loc": [-79.42848154284123, 43.641401675960374],
     "dst_loc": [-79.52745693913239, 43.750338501653374]},
    {"type": "call",
     "src_number": "123-4567",
     "dst_number": "426-4804",
     "time": "2018-01-01 01:01:06",
     "duration": 50,
     "src_loc": [-79.42848154284123, 43.641401675960374],
     "dst_loc": [-79.52745693913239, 43.750338501653374]},
    {"type": "call",
     "src_number": "123-4567",
     "dst_number": "426-4804",
     "time": "2018-02-01 01:01:06",
     "duration": 50,
     "src_loc": [-79.42848154284123, 43.641401675960374],
     "dst_loc": [-79.52745693913239, 43.750338501653374]}
],
    "customers": [
        {"lines": [{"number": "123-4567", "contract": "prepaid"}], "id": 5555},
        {"lines": [{"number": "426-4804", "contract": "prepaid"}], "id": 5678},
        {"lines": [{"number": "426-4805", "contract": "prepaid"}], "id": 1234}
    ]
}


def create_customers_2(log: dict[str, list[dict]]) -> list[Customer]:
    """ Returns a list of Customer instances for each customer from the input
    dataset from the dictionary <log>.

    Precondition:
    - The <log> dictionary contains the input data in the correct format,
    matching the expected input format described in the handout.
    """
    customer_list = []
    for cust in log['customers']:
        customer = Customer(cust['id'])
        for line in cust['lines']:
            contract = None
            if line['contract'] == 'prepaid':
                # start with $100 credit on the account
                contract = PrepaidContract(datetime.date(2017, 12,
                                                         25),
                                           100)
            elif line['contract'] == 'mtm':
                contract = MTMContract(datetime.date(2017, 12,
                                                     25))
            elif line['contract'] == 'term':
                contract = TermContract(datetime.date(2017, 12,
                                                      25),
                                        datetime.date(2019, 6,
                                                      25))
            else:
                print("ERROR: unknown contract type")

            line = PhoneLine(line['number'], contract)
            customer.add_phone_line(line)
        customer_list.append(customer)
    return customer_list


def test_prepaid_carry_over() -> None:
    customer = create_customers_2(test_dict_3)
    process_event_history(test_dict_3, customer)
    billi = customer[1].generate_bill(2, 2018)
    assert billi[1] == -100.0


def test_prepaid_carry_over_calls_made() -> None:
    customer = create_customers_2(test_dict_3)
    process_event_history(test_dict_3, customer)
    billi = customer[0].generate_bill(2, 2018)
    assert billi[1] == pytest.approx(-99.90)


test_dict_4 = {'events': [
    {"type": "call",
     "src_number": "426-4804",
     "dst_number": "123-4567",
     "time": "2018-01-01 01:01:04",
     "duration": 60,
     "src_loc": [-79.42848154284123, 43.641401675960374],
     "dst_loc": [-79.52745693913239, 43.750338501653374],
     },
    {"type": "call",
     "src_number": "426-4804",
     "dst_number": "123-4567",
     "time": "2018-02-01 01:01:05",
     "duration": 17940,
     "src_loc": [-79.42848154284123, 43.641401675960374],
     "dst_loc": [-79.52745693913239, 43.750338501653374]},
    {"type": "call",
     "src_number": "426-4804",
     "dst_number": "123-4567",
     "time": "2018-03-01 01:01:05",
     "duration": 18000,
     "src_loc": [-79.42848154284123, 43.641401675960374],
     "dst_loc": [-79.52745693913239, 43.750338501653374]}
],
    "customers": [
        {"lines": [{"number": "426-4804", "contract": "prepaid"}], "id": 5555},
        {"lines": [{"number": "123-4567", "contract": "term"}], "id": 5565},
    ]
}


def test_prepaid_carry_overs() -> None:
    customers = create_customers_2(test_dict_4)
    process_event_history(test_dict_4, customers)
    billi = customers[0].generate_bill(3, 2018)
    assert billi[1] == -100 + 15  # (-100 balance and 15 minutes billed)


if __name__ == '__main__':
    pytest.main(['a1_my_tests.py'])
