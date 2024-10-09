from datetime import *
from parse import tiny_data
from test_data import jan_data, com_data, customer, loc_data, filter_data
from contract import *
from customer import *
from phoneline import *
from filter import *
import unittest

LOW_COOR = (-79.697878, 43.576959)
HIGH_COOR = (-79.196382, 43.799568)


def create_customers(log: dict[str, list[dict]]) -> list[Customer]:
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
                contract = PrepaidContract(datetime.date(2017, 12, 25), 100)
            elif line['contract'] == 'mtm':
                contract = MTMContract(datetime.date(2017, 12, 25))
            elif line['contract'] == 'term':
                contract = TermContract(datetime.date(2017, 12, 25),
                                        datetime.date(2019, 6, 25))
            else:
                print("ERROR: unknown contract type")

            line = PhoneLine(line['number'], contract)
            customer.add_phone_line(line)
        customer_list.append(customer)
    return customer_list


def create_call(source: dict) -> list[Call]:
    res = []
    event_list = source["events"]
    for event_dict in event_list:
        if event_dict["type"] == "call":
            src_number = event_dict["src_number"]
            dst_number = event_dict["dst_number"]
            duration = event_dict["duration"]
            time = event_dict["time"]
            time = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
            src_loc = event_dict["src_loc"]
            dst_loc = event_dict["dst_loc"]
            call = Call(src_number, dst_number, time, duration, src_loc,
                        dst_loc)
            res.append(call)
    return res


class CallTest1(unittest.TestCase):
    def setUp(self):
        self.history = CallHistory()
        self.single_call = create_call(tiny_data)[0]

    def test_basic(self):
        self.assertDictEqual({}, self.history.incoming_calls)
        self.assertDictEqual({}, self.history.outgoing_calls)
        self.assertEqual(None,
                         self.history.register_incoming_call(self.single_call))
        self.assertEqual(None,
                         self.history.register_incoming_call(self.single_call))

    def test_incoming_1(self):
        call_list = create_call(tiny_data)
        for call in call_list:
            self.history.register_incoming_call(call)
        exp_res = {(1, 2018): [call_list[0]]}
        act_res = self.history.incoming_calls
        self.assertDictEqual(exp_res, act_res,
                             'The call should be registered to the incoming calls')

    def test_incoming_2(self):
        self.maxDiff = None
        call_list = [self.single_call]
        for call in call_list:
            self.history.register_incoming_call(call)
            self.history.register_incoming_call(call)
        exp_res = {(1, 2018): [call_list[0], call_list[0]]}
        act_res = self.history.incoming_calls
        self.assertDictEqual(exp_res, act_res,
                             'There should be two calls registered to the incoming calls')

    def test_incoming_3(self):
        call_list = create_call(jan_data)
        call_list.sort(key=lambda x: x.time)
        for call in call_list:
            self.history.register_incoming_call(call)
        exp_res = {(1, 2018): call_list}
        act_res = self.history.incoming_calls
        self.assertDictEqual(exp_res, act_res,
                             'Every call in the january should be registered to the incoming calls')

    def test_incoming_4(self):
        self.maxDiff = None
        call_list = create_call(com_data)
        call_list.sort(key=lambda x: x.time)
        for call in call_list:
            self.history.register_incoming_call(call)
        exp_res = {(1, 2018): [call_list[0]], (2, 2018): [call_list[1]],
                   (3, 2018): [call_list[2]], (4, 2018): [call_list[3]]}
        act_res = self.history.incoming_calls
        self.assertDictEqual(exp_res, act_res,
                             'Both January and March\'s calls(aka you have two keys) should be registered to the incoming calls')

    def test_outgoing_1(self):
        call_list = create_call(tiny_data)
        for call in call_list:
            self.history.register_outgoing_call(call)
        exp_res = {(1, 2018): [call_list[0]]}
        act_res = self.history.outgoing_calls
        self.assertDictEqual(exp_res, act_res,
                             'There is only one call should be registered to the outgoing calls')

    def test_outgoing_2(self):
        call_list = create_call(tiny_data)
        for call in call_list:
            self.history.register_outgoing_call(call)
            self.history.register_outgoing_call(call)
        exp_res = {(1, 2018): [call_list[0], call_list[0]]}
        act_res = self.history.outgoing_calls
        self.assertDictEqual(exp_res, act_res,
                             "Two calls should be registered to the outoing calls")

    def test_outgoing_3(self):
        call_list = create_call(jan_data)
        call_list.sort(key=lambda x: x.time)
        for call in call_list:
            self.history.register_outgoing_call(call)
        exp_res = {(1, 2018): call_list}
        act_res = self.history.outgoing_calls
        self.assertDictEqual(exp_res, act_res,
                             'Every call in the January should be registered to the history')

    def test_outgoing_4(self):
        call_list = create_call(com_data)
        call_list.sort(key=lambda x: x.time)
        for call in call_list:
            self.history.register_outgoing_call(call)
        exp_res = {(1, 2018): [call_list[0]], (2, 2018): [call_list[1]],
                   (3, 2018): [call_list[2]], (4, 2018): [call_list[3]]}
        act_res = self.history.outgoing_calls
        self.assertDictEqual(exp_res, act_res,
                             'Both of calls in the January and the March should be registered to the outgoing calls')


class CallTest2(unittest.TestCase):
    def setUp(self):
        self.contract = MTMContract(date(2018, 1, 12))
        self.phoneline = PhoneLine("441-4444", self.contract)
        self.single_call = create_call(tiny_data)[0]
        self.jan_data = sorted(create_call(jan_data), key=lambda x: x.time)
        self.com_data = sorted(create_call(com_data), key=lambda x: x.time)

    def test_basic(self):
        self.assertEqual(None, self.phoneline.make_call(self.single_call))
        self.assertEqual(None, self.phoneline.receive_call(self.single_call))

    def test_make_call(self):
        single_call = create_call(tiny_data)[0]
        self.phoneline.make_call(single_call)
        exp_res = {
            (single_call.time.month, single_call.time.year): [single_call]}
        act_res = self.phoneline.callhistory.outgoing_calls
        exp_key = [(single_call.time.month, single_call.time.year)]
        act_key = list(self.phoneline.bills.keys())
        exp_duration = ceil(single_call.duration / 60.0)
        act_duration = self.phoneline.contract.bill.billed_min
        self.assertDictEqual(exp_res, act_res,
                             'There is a single call should be registered to the outgoing calls of the the phoneline\'s history')
        self.assertCountEqual(exp_key, act_key,
                              'Check the month and years for the bill')
        self.assertEqual(exp_duration, act_duration,
                         "The duration of the call should be added to the billed minute")

    def test_make_call_2(self):
        jan_call = self.jan_data
        exp_month = jan_call[0].time.month
        exp_year = jan_call[1].time.year
        for call in jan_call:
            self.phoneline.make_call(call)
        exp_res = {(exp_month, exp_year): jan_call}
        act_res = self.phoneline.callhistory.outgoing_calls
        exp_key = [(exp_month, exp_year)]
        act_key = list(self.phoneline.bills.keys())
        exp_duration = ceil(sum([call.duration for call in jan_call]) / 60.0)
        act_duration = self.phoneline.contract.bill.billed_min
        self.assertDictEqual(exp_res, act_res,
                             'Every call in the January should be registered to the outgoing calls of the phoneline\'s history')
        self.assertCountEqual(exp_key, act_key,
                              'Check the month and years for the bill')
        self.assertEqual(exp_duration, act_duration,
                         'The duration of the calls in the january should be added to the billed minute')

    def test_make_call_3(self):
        com_data = self.com_data
        exp_res = {}
        exp_key = []
        exp_duration = 0
        act_duration = 0
        for call in com_data:
            self.phoneline.make_call(call)
            m_y_tuple = call.get_bill_date()
            temp = exp_res.get(m_y_tuple, [])
            temp.append(call)
            exp_res[m_y_tuple] = temp
            exp_key.append(m_y_tuple)
            exp_duration += call.duration
            act_duration += self.contract.bill.billed_min
        act_res = self.phoneline.callhistory.outgoing_calls
        act_key = list(self.phoneline.bills.keys())
        self.assertDictEqual(exp_res, act_res,
                             'You should register calls to the outgoing calls')
        self.assertCountEqual(exp_key, act_key,
                              'Check the month and years for the bills')
        self.assertEqual(ceil(exp_duration / 60.0), act_duration,
                         'This checks the sum of total durations')

    def test_receive_call(self):
        single_call = create_call(tiny_data)[0]
        self.phoneline.receive_call(single_call)
        exp_res = {
            (single_call.time.month, single_call.time.year): [single_call]}
        act_res = self.phoneline.callhistory.incoming_calls
        exp_key = [(single_call.time.month, single_call.time.year)]
        act_key = list(self.phoneline.bills.keys())
        self.assertDictEqual(exp_res, act_res,
                             'The single call should be registered to the incoming calls of the history')
        self.assertCountEqual(exp_key, act_key,
                              'Check the month and years for the bill')

    def test_receive_call_2(self):
        jan_call = self.jan_data
        exp_month = jan_call[0].time.month
        exp_year = jan_call[1].time.year
        for call in jan_call:
            self.phoneline.receive_call(call)
        exp_res = {(exp_month, exp_year): jan_call}
        act_res = self.phoneline.callhistory.incoming_calls
        exp_key = [(exp_month, exp_year)]
        act_key = list(self.phoneline.bills.keys())
        self.assertDictEqual(exp_res, act_res,
                             'Every call in the January should be registered to the incoming calls of the history')
        self.assertCountEqual(exp_key, act_key,
                              'Check the month and years for the bill')

    def test_receive_call_3(self):
        com_data = self.com_data
        exp_res = {}
        exp_key = []
        for call in com_data:
            self.phoneline.receive_call(call)
            m_y_tuple = call.get_bill_date()
            temp = exp_res.get(m_y_tuple, [])
            temp.append(call)
            exp_res[m_y_tuple] = temp
            exp_key.append(m_y_tuple)
        act_res = self.phoneline.callhistory.incoming_calls
        act_key = list(self.phoneline.bills.keys())
        self.assertDictEqual(exp_res, act_res,
                             'Calls in the January and March should be registered to the incoming calls')
        print(com_data)
        print(exp_key)
        print(act_key)
        self.assertCountEqual(exp_key, act_key,
                              'Check the month and years for the bill')


class PhoneLineTest(unittest.TestCase):
    def setUp(self):
        self.customer = Customer(2012)
        self.contract = MTMContract(date(2018, 1, 12))
        self.customer.add_phone_line(PhoneLine("422-4785", self.contract))
        self.customer.add_phone_line(PhoneLine("136-5226", self.contract))
        self.single_call = create_call(tiny_data)[0]
        self.jan_call = create_call(jan_data)
        self.com_call = create_call(com_data)

    def test_basic(self):
        self.customer.receive_call(self.single_call)
        self.assertEqual(None, self.customer.make_call(self.single_call))
        self.assertEqual(None, self.customer.receive_call(self.single_call))

    def test_make_call_1(self):
        self.customer.make_call(self.single_call)
        # Test bill is added to a new list
        self.assertEqual(True,
                         list(self.customer._phone_lines[0].bills.keys()) == [
                             (1, 2018)],
                         'The phone co-responding to the src number should add a bill')
        # Test add bill to the contract
        self.assertEqual(True, self.customer._phone_lines[
            0].contract.bill.type == "MTM")
        self.assertEqual(True, self.customer._phone_lines[
            0].contract.bill.fixed_cost == 50.00)
        self.assertEqual(True, self.customer._phone_lines[
            0].contract.bill.min_rate == 0.05)
        # Test register the call to the history
        self.assertCountEqual([(1, 2018)], list(
            self.customer._phone_lines[0].callhistory.outgoing_calls.keys()),
                              'There is only one call got registered to the outgoing call of the co-responding phoneline')
        # Test the added minutes
        self.assertCountEqual([self.single_call], self.customer._phone_lines[
            0].callhistory.outgoing_calls[(1, 2018)],
                              'There is only one call in the month got registered to the outgoing calls')
        # Test bill call
        self.assertEqual(2, self.contract.bill.billed_min,
                         'The duration of the call is the billed min of the bill')

    def test_make_call_2(self):
        self.customer.add_phone_line(
            PhoneLine("731-0105", MTMContract(date(2018, 1, 12))))
        self.customer.add_phone_line(
            PhoneLine("934-0592", MTMContract(date(2018, 1, 12))))
        self.customer.add_phone_line(
            PhoneLine("136-5226", MTMContract(date(2018, 1, 12))))
        self.customer.add_phone_line(
            PhoneLine("420-4785", MTMContract(date(2018, 1, 12))))
        for call in self.jan_call:
            self.customer.make_call(call)
        # Test register call
        self.assertCountEqual([self.jan_call[0], self.jan_call[2]],
                              self.customer._phone_lines[
                                  0].callhistory.outgoing_calls[(1, 2018)],
                              'Calls should be registered into the outgoing calls of the co-responding phoneline with same src-number'
                              )
        self.assertCountEqual([self.jan_call[1]], self.customer._phone_lines[
            3].callhistory.outgoing_calls[(1, 2018)],
                              'Calls should be registered into the outgoing calls of the co-responding phoneline with same src-number'
                              )
        self.assertCountEqual([self.jan_call[-1]], self.customer._phone_lines[
            -1].callhistory.outgoing_calls[(1, 2018)],
                              'Calls should be registered into the outgoing calls of the co-responding phoneline with same src-number'
                              )
        # Test bill call
        self.assertEqual(4,
                         self.customer._phone_lines[0].contract.bill.billed_min,
                         'The duration of the call should be the billed min of the bill')
        self.assertEqual(2,
                         self.customer._phone_lines[3].contract.bill.billed_min,
                         'The duration of the call should be the billed min of the bill')
        self.assertEqual(2, self.customer._phone_lines[
            -1].contract.bill.billed_min,
                         'The duration of the call should be the billed min of the bill')

    def test_make_call_3(self):
        self.customer.add_phone_line(
            PhoneLine("731-0105", MTMContract(date(2018, 1, 12))))
        self.customer.add_phone_line(
            PhoneLine("934-0592", MTMContract(date(2018, 2, 12))))
        self.customer.add_phone_line(
            PhoneLine("420-4785", MTMContract(date(2018, 4, 12))))
        for call in self.com_call:
            self.customer.make_call(call)
        self.assertCountEqual([(1, 2018), (3, 2018)],
                              list(self.customer._phone_lines[0].bills.keys()),
                              'Test the bill month for the src-number')
        self.assertCountEqual([(2, 2018)],
                              list(self.customer._phone_lines[3].bills.keys()),
                              'Test the bill month for the src-number')
        self.assertCountEqual([(4, 2018)],
                              list(self.customer._phone_lines[-1].bills.keys()),
                              'Test the bill month for the src-number')

    def test_receive_call(self):
        self.customer.receive_call(self.single_call)
        self.assertEqual(True,
                         list(self.customer._phone_lines[1].bills.keys()) == [
                             (1, 2018)],
                         'The call should be registered to the co-responding phoneline with same dst-number')
        self.assertEqual(True,
                         self.customer._phone_lines[
                             1].contract.bill.type == "MTM")
        self.assertEqual(True,
                         self.customer._phone_lines[
                             1].contract.bill.fixed_cost == 50.00)
        self.assertEqual(True,
                         self.customer._phone_lines[
                             1].contract.bill.min_rate == 0.05)
        # Test register the call to the history
        self.assertCountEqual([(1, 2018)], list(self.customer._phone_lines[
                                                    1].callhistory.incoming_calls.keys()))
        # Test the added minutes
        self.assertCountEqual([self.single_call],
                              self.customer._phone_lines[
                                  1].callhistory.incoming_calls[(1, 2018)])
        self.assertEqual(0,
                         self.customer._phone_lines[1].contract.bill.billed_min,
                         'The incoming call should not be billed')

    def test_receive_call_2(self):
        self.customer.add_phone_line(
            PhoneLine("731-0105", MTMContract(date(2018, 1, 12))))
        self.customer.add_phone_line(
            PhoneLine("934-0592", MTMContract(date(2018, 1, 12))))
        self.customer.add_phone_line(
            PhoneLine("420-4785", MTMContract(date(2018, 1, 12))))
        self.customer.add_phone_line(
            PhoneLine("137-5226", MTMContract(date(2018, 1, 12))))
        for call in self.jan_call:
            self.customer.receive_call(call)
        self.assertCountEqual([self.jan_call[0]], self.customer._phone_lines[
            2].callhistory.incoming_calls[(1, 2018)],
                              'Check the proper incoming_calls for the phoneline')
        self.assertCountEqual([self.jan_call[1], self.jan_call[2]],
                              self.customer._phone_lines[
                                  1].callhistory.incoming_calls[(1, 2018)])
        self.assertCountEqual([self.jan_call[-1]], self.customer._phone_lines[
            -1].callhistory.incoming_calls[(1, 2018)])


unittest.main(exit=False)


class TermTest(unittest.TestCase):
    def setUp(self):
        self.exp_start = date(2018, 1, 1)
        self.exp_end = date(2018, 3, 28)
        self.contract = TermContract(self.exp_start, self.exp_end)
        self.jan_call = create_call(jan_data)
        self.assertEqual(self.exp_start, self.contract.start)
        self.assertEqual(None, self.contract.bill)
        self.temp_bill = Bill()

    def test_basic(self):
        self.assertEqual(self.exp_start, self.contract.start)
        self.assertEqual(None, self.contract.bill)
        self.assertEqual(None, self.contract.new_month(2, 2018, Bill()))
        self.assertEqual(True,
                         isinstance(self.contract.cancel_contract(), float))

    def test_new_month_1(self):
        self.assertEqual(None, self.contract.new_month(1, 2018, self.temp_bill))
        self.assertEqual(True, self.contract.bill == self.temp_bill)
        self.assertEqual(0, self.contract.bill.free_min)
        self.assertEqual(0.1, self.contract.bill.min_rate)

    def test_new_month_2(self):
        self.contract.new_month(1, 2018, Bill())
        temp_bill = Bill()
        self.contract.new_month(2, 2018, temp_bill)
        self.assertEqual(0, self.contract.bill.free_min)
        self.assertEqual(0.1, self.contract.bill.min_rate)
        self.assertEqual(20, self.contract.bill.fixed_cost)

    def test_new_month_3(self):
        self.contract.new_month(1, 2018, Bill())
        temp_bill = Bill()
        temp_bill.add_fixed_cost(20)
        self.contract.new_month(2, 2018, Bill())
        self.contract.new_month(3, 2018, temp_bill)
        self.assertEqual(0, self.contract.bill.free_min)
        self.assertEqual(0.1, self.contract.bill.min_rate)
        self.assertEqual(40, self.contract.bill.fixed_cost)

    def test_bill_call(self):
        self.contract.new_month(1, 2018, Bill())
        self.contract.bill_call(self.jan_call[0])
        self.assertEqual(2, self.contract.bill.free_min)
        self.assertEqual(0, self.contract.bill.billed_min)

    def test_bill_call_2(self):
        self.contract.new_month(1, 2018, Bill())
        for call in self.jan_call:
            self.contract.bill_call(call)
        self.assertEqual(8, self.contract.bill.free_min)
        self.assertEqual(0, self.contract.bill.billed_min)

    def test_bill_call_3(self):
        self.contract.new_month(2, 2018, Bill())
        for i in range(15):
            for call in self.jan_call:
                self.contract.bill_call(call)
        self.assertEqual(100, self.contract.bill.free_min)
        self.assertEqual(20, self.contract.bill.billed_min)

    def test_cancel_contract(self):
        self.contract.new_month(1, 2018, Bill())
        exp_res = 320
        act_res = self.contract.cancel_contract()
        self.assertEqual(exp_res, act_res,
                         "There is no call in the first month and no deposit should be refund")

    def test_cancel_contract_2(self):
        self.contract.new_month(2, 2018, Bill())
        exp_res = 20
        act_res = self.contract.cancel_contract()
        self.assertEqual(exp_res, act_res,
                         "You should return the deposit after the term date")

    def test_cancel_contract_3(self):
        self.contract.new_month(2, 2018, Bill())
        for i in range(15):
            for call in self.jan_call:
                self.contract.bill_call(call)
        exp_res = 22
        act_res = self.contract.cancel_contract()
        self.assertEqual(exp_res, act_res,
                         "You should return the deposit even after the term date")

    def test_cancel_contract_4(self):
        self.contract.new_month(3, 2018, Bill())
        for i in range(15):
            for call in self.jan_call:
                self.contract.bill_call(call)
        exp_res = 22
        act_res = self.contract.cancel_contract()
        self.assertEqual(exp_res, act_res,
                         "You should return the deposit even after the term date")

    def test_cancel_contract_5(self):
        self.contract.new_month(4, 2018, Bill())
        for i in range(15):
            for call in self.jan_call:
                self.contract.bill_call(call)
        exp_res = -278
        act_res = self.contract.cancel_contract()
        self.assertEqual(exp_res, act_res,
                         "You should return the deposit even after the term date")

    def test_cancel_contract_6(self):
        contract = TermContract(date(2018, 1, 1), date(2018, 1, 18))
        temp_bill = Bill()
        temp_bill.add_fixed_cost(20)
        contract.new_month(1, 2018, Bill())
        exp_res = 320
        act_res = contract.cancel_contract()
        self.assertEqual(exp_res, act_res, "You should not return the deposit")

    def test_cancel_contract_7(self):
        contract = TermContract(date(2018, 1, 1), date(2018, 2, 18))
        contract.new_month(1, 2018, Bill())
        temp_bill = Bill()
        contract.new_month(2, 2018, temp_bill)
        exp_res = 20
        act_res = contract.cancel_contract()
        self.assertEqual(exp_res, act_res,
                         "You should not return the deposit and charged the fixed cost")

    def test_cancel_contract_8(self):
        contract = TermContract(date(2018, 1, 1), date(2018, 2, 28))
        contract.new_month(1, 2018, Bill())
        temp_bill = Bill()
        contract.new_month(2, 2018, Bill())
        temp_bill.add_fixed_cost(30)
        contract.new_month(3, 2018, temp_bill)
        exp_res = -250
        act_res = contract.cancel_contract()
        self.assertEqual(exp_res, act_res, "You should  return the deposit")


class MTMTest(unittest.TestCase):
    def setUp(self):
        self.exp_start = date(2017, 1, 12)
        self.contract = MTMContract(date(2017, 1, 12))
        self.jan_call = create_call(jan_data)
        self.temp_bill = Bill()
        self.assertEqual(self.exp_start, self.contract.start)
        self.assertEqual(None, self.contract.bill)

    def test_new_month_1(self):
        self.assertEqual(None, self.contract.new_month(1, 2018, self.temp_bill))
        self.assertEqual(True, self.contract.bill == self.temp_bill)
        self.assertEqual(0, self.contract.bill.free_min)
        self.assertEqual(0.05, self.contract.bill.min_rate)
        self.assertEqual(50, self.contract.bill.fixed_cost)

    def test_new_month_2(self):
        self.contract.new_month(1, 2018, Bill())
        temp_bill = Bill()
        self.contract.new_month(2, 2018, temp_bill)
        self.assertEqual(0, self.contract.bill.free_min)
        self.assertEqual(0.05, self.contract.bill.min_rate)
        self.assertEqual(50, self.contract.bill.fixed_cost)

    def test_new_month_3(self):
        self.contract.new_month(1, 2018, Bill())
        temp_bill = Bill()
        temp_bill.add_fixed_cost(20)
        self.contract.new_month(2, 2018, Bill())
        self.contract.new_month(3, 2018, temp_bill)
        self.assertEqual(0, self.contract.bill.free_min)
        self.assertEqual(0.05, self.contract.bill.min_rate)
        self.assertEqual(70, self.contract.bill.fixed_cost)

    def test_bill_call(self):
        self.contract.new_month(1, 2018, Bill())
        self.contract.bill_call(self.jan_call[0])
        self.assertEqual(0, self.contract.bill.free_min)
        self.assertEqual(2, self.contract.bill.billed_min)

    def test_bill_call_2(self):
        self.contract.new_month(1, 2018, Bill())
        for call in self.jan_call:
            self.contract.bill_call(call)
        self.assertEqual(0, self.contract.bill.free_min)
        self.assertEqual(8, self.contract.bill.billed_min)

    def test_bill_call_3(self):
        self.contract.new_month(2, 2018, Bill())
        for i in range(15):
            for call in self.jan_call:
                self.contract.bill_call(call)
        self.assertEqual(0, self.contract.bill.free_min)
        self.assertEqual(120, self.contract.bill.billed_min)

    def test_cancel_contract(self):
        self.contract.new_month(1, 2018, Bill())
        exp_res = 50
        act_res = self.contract.cancel_contract()
        self.assertEqual(exp_res, act_res,
                         "There is no call in the first month and you should be charged with full amout of MTM fee")

    def test_cancel_contract_2(self):
        self.contract.new_month(2, 2018, Bill())
        exp_res = 50
        act_res = self.contract.cancel_contract()
        self.assertEqual(exp_res, act_res,
                         "There is no call in the first month and you should be charged with full amout of MTM fee")

    def test_cancel_contract_3(self):
        self.contract.new_month(3, 2018, Bill())
        for i in range(15):
            for call in self.jan_call:
                self.contract.bill_call(call)
        exp_res = 56
        act_res = self.contract.cancel_contract()
        self.assertEqual(exp_res, act_res,
                         "There is no call in the first month and you should be charged with full amout of MTM fee")


class PrepaidTest(unittest.TestCase):
    def setUp(self):
        self.exp_start = date(2017, 1, 12)
        self.contract = PrepaidContract(date(2017, 1, 12), balance=50)
        self.jan_call = create_call(jan_data)
        self.temp_bill = Bill()
        self.contract.new_month(1, 2017, self.temp_bill)
        self.assertEqual(self.exp_start, self.contract.start)
        self.assertEqual(self.temp_bill, self.contract.bill)

    def test_new_month(self):
        self.assertEqual(-50, self.contract.bill.fixed_cost)
        self.assertEqual(0.025, self.contract.bill.min_rate)
        self.assertEqual(0, self.contract.bill.billed_min)
        self.assertEqual(0, self.contract.bill.free_min)

    def test_new_month_2(self):
        temp_bill = Bill()
        temp_bill.add_fixed_cost(25)
        self.contract.new_month(2, 2017, temp_bill)
        self.assertEqual(-25, self.contract.bill.fixed_cost)

    def test_new_month_3(self):
        temp_bill = Bill()
        temp_bill.add_fixed_cost(25)
        self.contract.new_month(2, 2017, temp_bill)
        temp_bill_2 = Bill()
        temp_bill_2.add_fixed_cost(-25)
        self.contract.new_month(3, 2017, temp_bill_2)
        self.assertEqual(-50, self.contract.bill.fixed_cost)

    def test_new_month_4(self):
        temp_bill = Bill()
        temp_bill.add_fixed_cost(41)
        self.contract.new_month(2, 2017, temp_bill)
        self.assertEqual(-9, self.contract.bill.fixed_cost)
        temp_bill_2 = Bill()
        temp_bill_2.add_fixed_cost(-9)
        self.contract.new_month(3, 2017, temp_bill_2)
        self.assertEqual(-43, self.contract.bill.fixed_cost)

    def test_new_month_5(self):
        temp_bill = Bill()
        temp_bill.add_fixed_cost(41)
        self.contract.new_month(2, 2017, temp_bill)
        self.assertEqual(-9, self.contract.bill.fixed_cost)
        temp_bill_2 = Bill()
        temp_bill_2.add_fixed_cost(41)
        self.contract.new_month(3, 2017, temp_bill_2)
        self.assertEqual(7, self.contract.bill.fixed_cost)

    def test_new_month_6(self):
        temp_bill = Bill()
        temp_bill.add_fixed_cost(25)
        self.contract.new_month(2, 2017, temp_bill)
        temp_bill_2 = Bill()
        temp_bill_2.add_fixed_cost(25)
        self.contract.new_month(3, 2017, temp_bill_2)
        self.assertEqual(0, self.contract.bill.fixed_cost)

    def test_bill_call(self):
        self.contract.new_month(1, 2018, Bill())
        self.contract.bill_call(self.jan_call[0])
        self.assertEqual(0, self.contract.bill.free_min)
        self.assertEqual(2, self.contract.bill.billed_min)

    def test_bill_call_2(self):
        self.contract.new_month(1, 2018, Bill())
        for call in self.jan_call:
            self.contract.bill_call(call)
        self.assertEqual(0, self.contract.bill.free_min)
        self.assertEqual(8, self.contract.bill.billed_min)

    def test_bill_call_3(self):
        self.contract.new_month(2, 2018, Bill())
        for i in range(15):
            for call in self.jan_call:
                self.contract.bill_call(call)
        self.assertEqual(0, self.contract.bill.free_min)
        self.assertEqual(120, self.contract.bill.billed_min)

    def test_cancel_contract(self):
        exp_res = 0
        act_res = self.contract.cancel_contract()
        self.assertEqual(exp_res, act_res,
                         "The prepaid value will not be returned")

    def test_cancel_contract_2(self):
        temp_bill = Bill()
        temp_bill.add_fixed_cost(41)
        temp_bill.add_billed_minutes(400)
        self.contract.new_month(2, 2017, temp_bill)
        exp_res = 1
        act_res = self.contract.cancel_contract()
        self.assertEqual(exp_res, act_res,
                         "The billed cost is 51 and credit is 50 you still own the company 1")

    def test_cancel_contract_3(self):
        temp_bill = Bill()
        temp_bill.add_fixed_cost(41)
        self.contract.new_month(2, 2017, temp_bill)
        temp_bill_2 = Bill()
        temp_bill_2.add_fixed_cost(41)
        self.contract.new_month(3, 2017, temp_bill_2)
        temp_bill.add_billed_minutes(100)
        self.assertEqual(7, self.contract.cancel_contract(),
                         "YOu still own the company")

    def test_cancel_contract_4(self):
        temp_bill = Bill()
        temp_bill.add_fixed_cost(41)
        self.contract.new_month(1, 2017, temp_bill)
        temp_bill_2 = Bill()
        temp_bill_2.add_fixed_cost(24)
        self.contract.new_month(2, 2017, temp_bill_2)
        act_res = self.contract.cancel_contract()
        self.assertEqual(0, act_res, "The credit will not be returned")


unittest.main(exit=False)


class CustomerFilterTest(unittest.TestCase):
    def setUp(self):
        self.filter = CustomerFilter()
        self.customer = create_customers(customer)
        self.jan_call = create_call(filter_data)
        self.customer[3].make_call(self.jan_call[0])
        self.customer[1].make_call(self.jan_call[1])
        self.customer[3].make_call(self.jan_call[2])
        self.customer[4].receive_call(self.jan_call[0])
        self.customer[3].receive_call(self.jan_call[1])
        self.customer[3].receive_call(self.jan_call[2])

    def test_basic(self):
        act_res = self.filter.apply(self.customer, self.jan_call[-1:], "5716")
        exp_res = self.jan_call[-1:]
        self.assertCountEqual(exp_res, act_res,
                              "Return every call in the list that have the same src-number / dst-number associated with numbers in Uers's phonlines")

    def test_basic_2(self):
        act_res = self.filter.apply(self.customer, self.jan_call, "9701")
        exp_res = []
        self.assertCountEqual(self.jan_call[0:1], act_res,
                              "Return every call in the list that have the same src-number / dst-number associated with numbers in Uers's phonlines")
        act_res = self.filter.apply(self.customer, self.jan_call, "8548")
        self.assertCountEqual(exp_res, act_res,
                              "Return every call in the list that have the same src-number / dst-number associated with numbers in Uers's phonlines")
        act_res = self.filter.apply(self.customer, self.jan_call, "2247")
        self.assertCountEqual(exp_res, act_res,
                              "Return every call in the list that have the same src-number / dst-number associated with numbers in Uers's phonlines")

    def test_basic_3(self):
        act_res = self.filter.apply(self.customer, self.jan_call, "5716")
        exp_res = [self.jan_call[0], self.jan_call[1], self.jan_call[2]]
        self.assertCountEqual(exp_res, act_res,
                              "Return every call in the list that have the same src-number / dst-number associated with numbers in Uers's phonlines")
        exp_res = [self.jan_call[1]]
        act_res = self.filter.apply(self.customer, self.jan_call, "3895")
        self.assertCountEqual(exp_res, act_res,
                              "Return every call in the list that have the same src-number / dst-number associated with numbers in Uers's phonlines")

    def test_invalid(self):
        act_res = self.filter.apply(self.customer, self.jan_call[-1:],
                                    "sdhfsdjn")
        self.assertEqual(True, act_res == self.jan_call[-1:],
                         "Return the orginal list since the user id is invalid")
        act_res = self.filter.apply(self.customer, self.jan_call[-1:], "")
        self.assertEqual(True, act_res == self.jan_call[-1:],
                         "Return the orginal list since the user id is invalid")
        act_res = self.filter.apply(self.customer, self.jan_call[-1:], "abcd")
        self.assertEqual(True, act_res == self.jan_call[-1:],
                         "Return the orginal list since the user id is invalid")
        act_res = self.filter.apply(self.customer, self.jan_call, "abc1")
        exp_res = self.jan_call
        self.assertCountEqual(exp_res, act_res,
                              "Return the orginal list since the user id is invalid")
        act_res = self.filter.apply(self.customer, self.jan_call, "9999")
        self.assertEqual(True, act_res == self.jan_call,
                         "Return the orginal list since the user id is invalid")


class DurationFilterTest(unittest.TestCase):
    def setUp(self):
        self.filter = DurationFilter()
        self.customer = create_customers(customer)
        self.jan_call = create_call(filter_data)
        self.customer[3].make_call(self.jan_call[0])
        self.customer[1].make_call(self.jan_call[1])
        self.customer[3].make_call(self.jan_call[2])
        self.customer[4].receive_call(self.jan_call[0])
        self.customer[3].receive_call(self.jan_call[1])
        self.customer[3].receive_call(self.jan_call[2])

    def test_basic(self):
        act_res = self.filter.apply(self.customer, [self.jan_call[0]], "L120")
        exp_res = [self.jan_call[0]]
        self.assertCountEqual(exp_res, act_res,
                              "Return every call in the list which less than 120")
        act_res = self.filter.apply(self.customer, [self.jan_call[0]], "G120")
        self.assertCountEqual([], act_res,
                              "Return every call in the list which grater than 120")
        act_res = self.filter.apply(self.customer, [self.jan_call[0]], 'G100')
        self.assertCountEqual(exp_res, act_res,
                              "Return every call in the list which grater than 100")
        act_res = self.filter.apply(self.customer, [self.jan_call[0]], "L100")
        self.assertCountEqual([], act_res,
                              "Return every call in the list which less than 100")

    def test_basic_2(self):
        act_res = self.filter.apply(self.customer, self.jan_call, "G110")
        self.assertCountEqual(self.jan_call, act_res,
                              "Return every call in the list which grater than 120")
        act_res = self.filter.apply(self.customer, self.jan_call, "L120")
        self.assertCountEqual(self.jan_call, act_res,
                              "Return every call in the list which less than 120")
        act_res = self.filter.apply(self.customer, self.jan_call, "L100")
        self.assertCountEqual([], act_res,
                              "Return every call in the list which less than 100")
        act_res = self.filter.apply(self.customer, self.jan_call, "G200")
        self.assertCountEqual([], act_res,
                              "Return every call in the list which grater than 200")
        act_res = self.filter.apply(self.customer, self.jan_call, "G50")
        self.assertEqual(self.jan_call, act_res,
                         "Return every call in the list greater than 50")
        act_res = self.filter.apply(self.customer, self.jan_call, "L001")
        self.assertEqual([], act_res, "Return empty list")

    def test_basic_3(self):
        act_res = self.filter.apply(self.customer, self.jan_call, "L118")
        exp_res = [self.jan_call[-1]]
        self.assertCountEqual(exp_res, act_res,
                              "Return every call in the list which less than 118")
        act_res = self.filter.apply(self.customer, self.jan_call, "G118")
        self.assertCountEqual([self.jan_call[1]], act_res,
                              "Return every call in the list which grater than 118")
        act_res = self.filter.apply(self.customer, self.jan_call, "L119")
        exp_res = [self.jan_call[0], self.jan_call[-1]]
        self.assertCountEqual(exp_res, act_res,
                              "Return every call in the list which less than 119")
        act_res = self.filter.apply(self.customer, self.jan_call, "L120")
        self.assertCountEqual(self.jan_call, act_res,
                              "Return every call in the list which less than 120")
        act_res = self.filter.apply(self.customer, self.jan_call, "G117")
        exp_res = self.jan_call[0:2]
        self.assertCountEqual(exp_res, act_res,
                              "Return every call in the list which greater than 117")

    def test_invalid(self):
        act_res = self.filter.apply(self.customer, [self.jan_call[0]],
                                    "sdhfsdjn")
        self.assertEqual(True, act_res == [self.jan_call[0]],
                         "Return the orginal list since the filter string is invalid")
        act_res = self.filter.apply(self.customer, [self.jan_call[0]], "")
        self.assertEqual(True, act_res == [self.jan_call[0]],
                         "Return the orginal list since the filter string is invalid")
        act_res = self.filter.apply(self.customer, [self.jan_call[0]], "g131")
        self.assertEqual(True, act_res == [self.jan_call[0]],
                         "Return the orginal list since the filter string is invalid")
        act_res = self.filter.apply(self.customer, [self.jan_call[0]], "l999")
        self.assertEqual(True, act_res == [self.jan_call[0]],
                         "Return the orginal list since the filter string is invalid")
        act_res = self.filter.apply(self.customer, [self.jan_call[0]], "Lb99")
        self.assertEqual(True, act_res == [self.jan_call[0]],
                         "Return the orginal list since the filter string is invalid")
        act_res = self.filter.apply(self.customer, [self.jan_call[0]], "G9b9")
        self.assertEqual(True, act_res == [self.jan_call[0]],
                         "Return the orginal list since the filter string is invalid")


class LocationFilterTest(unittest.TestCase):
    def setUp(self):
        self.filter = LocationFilter()
        self.customer = create_customers(customer)
        self.jan_call = create_call(jan_data)
        self.loc_data = create_call(loc_data)
        self.customer[3].make_call(self.loc_data[0])
        self.customer[1].make_call(self.loc_data[1])
        self.customer[3].make_call(self.loc_data[2])
        self.customer[4].receive_call(self.loc_data[0])
        self.customer[3].receive_call(self.loc_data[1])
        self.customer[3].receive_call(self.loc_data[2])

    def test_basic_1(self):
        act_res = self.filter.apply(self.customer, self.loc_data[-1:],
                                    "-79.68, 43.6, -79.679, 43.7")
        self.assertCountEqual([], act_res,
                              "Return every call in the list in the boundary")
        act_res = self.filter.apply(self.customer, self.loc_data[-1:],
                                    "-79.7, 43.6, -79.5, 43.64")
        self.assertCountEqual(self.loc_data[-1:], act_res,
                              "Return empty list since neither the src not dst are in the boundary")
        act_res = self.filter.apply(self.customer, self.loc_data,
                                    "-100, 80, -50, 90")
        self.assertEqual(self.loc_data, act_res, "Return everything")

    def test_basic_2(self):
        act_res = self.filter.apply(self.customer, self.loc_data,
                                    "-79.5, 43.61, -79.2, 43.799")
        exp_res = self.loc_data[1:]
        self.assertCountEqual(exp_res, act_res,
                              "Return the call in the list within the given boundary")
        act_res = self.filter.apply(self.customer, self.loc_data,
                                    "-79.21, 43.58, -79.20, 43.68")
        self.assertCountEqual([], act_res, "Return empty list")
        act_res = self.filter.apply(self.customer, self.loc_data,
                                    "-79.60, 43.577, -79.2, 43.78")
        self.assertCountEqual(self.loc_data, act_res,
                              "Return every call in the list in the boundary")

    def test_basic_3(self):
        act_res = self.filter.apply(self.customer, self.loc_data,
                                    "-79.68, 43.58, -79.679, 43.581")
        self.assertCountEqual([], act_res, "Return empty list")
        act_res = self.filter.apply(self.customer, self.loc_data,
                                    "-79.60, 43.58, -79.58, 43.60")
        self.assertCountEqual(self.loc_data[0:1], act_res,
                              "Return the call in the boundary even only src is in the boundary")
        act_res = self.filter.apply(self.customer, self.loc_data,
                                    "-79.58, 43.58, -79.579, 43.581")
        self.assertCountEqual(self.loc_data[0:1], act_res,
                              "Return the call in the boundary even only dst is in the boundary")
        act_res = self.filter.apply(self.customer, self.loc_data,
                                    "-79.479, 43.62, -79.39, 43.641")
        self.assertCountEqual(self.loc_data[1:2], act_res,
                              "Return the call in the boundary even only src is in the boundary")
        act_res = self.filter.apply(self.customer, self.loc_data,
                                    "-79.47, 43.63, -79.39, 43.64")
        self.assertCountEqual(self.loc_data[1:2], act_res,
                              "Return the call in the boundary even only dst is in the boundary")
        act_res = self.filter.apply(self.customer, self.loc_data,
                                    "-79.58, 43.58, -79.479, 43.62")
        exp_res = self.loc_data[0:2]
        self.assertCountEqual(exp_res, act_res, "Return calls in the boundary")
        act_res = self.filter.apply(self.customer, self.loc_data,
                                    "-79.49, 43.59, -79.39, 43.64")
        self.assertCountEqual(exp_res, act_res, "Return calls in the boundary")
        act_res = self.filter.apply(self.customer, self.loc_data,
                                    "-79.48, 43.63, -79.379, 43.661")
        exp_res = self.loc_data[1:3]
        self.assertCountEqual(exp_res, act_res, "Return calls in the boundary")
        act_res = self.filter.apply(self.customer, self.loc_data,
                                    "-79.60, 43.58, -79.29, 43.67")
        exp_res = self.loc_data
        self.assertCountEqual(exp_res, act_res, "Return calls in the boundary")

    def test_invalid(self):
        act_res = self.filter.apply(self.customer, self.loc_data,
                                    "-79.48,43.63,-79.379,43.661")
        self.assertEqual(True, act_res == self.loc_data,
                         "Return the original list")
        act_res = self.filter.apply(self.customer, self.loc_data,
                                    "-100, 40, -100, 40")
        self.assertEqual(True, act_res == self.loc_data,
                         "Return the original list since it out of boundary")
        act_res = self.filter.apply(self.customer, self.loc_data[-1:],
                                    "sdhfsdjn")
        self.assertEqual(True, act_res == self.loc_data[-1:],
                         "Return the orginal list since the filter string is invalid")
        act_res = self.filter.apply(self.customer, self.loc_data[-1:], "")
        self.assertEqual(True, act_res == self.loc_data[-1:],
                         "Return the orginal list since the filter string is invalid")
        act_res = self.filter.apply(self.customer, self.loc_data[-1:],
                                    "abcd, bcde, fghi")
        self.assertEqual(True, act_res == self.loc_data[-1:],
                         "Return the orginal list since the filter string is invalid")
        act_res = self.filter.apply(self.customer, self.loc_data[-1:],
                                    "abcd, bcde, gfik, xksd")
        self.assertEqual(True, act_res == self.loc_data[-1:],
                         "Return the orginal list since the filter string is "
                         "invalid")
        act_res = self.filter.apply(self.customer, self.loc_data[-1:],
                                    "123b, 456c, 321d, 459s")
        self.assertEqual(True, act_res == self.loc_data[-1:],
                         "Return the orginal list since the filter string is "
                         "invalid")


unittest.main(exit=False)

if __name__ == "__main__":
    unittest.main(['testing.py'])
