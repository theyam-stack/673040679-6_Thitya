"""
Thitiya Meengoen
673040679-6
P2
"""
class BankAccount:
    # Class attribute
    branch_name = "KKU Complex"
    branch_number = 1724
    last_loan_number = 0
    last_saving_number = 0
    # Private class attributes
    # account types
    __type_saving = 1
    __type_loan = 2

    # Constructor
    def __init__(self, name, account_number=0, type='saving', balance=0):
        self.name = name
        self._type = type
        self.account_number = account_number
        self.balance = balance

        if self._type == 'saving':
            BankAccount.last_saving_number += 1
            self.account_number = BankAccount.last_saving_number

        elif self._type == 'loan':
            BankAccount.last_loan_number += 1
            self.account_number = BankAccount.last_loan_number
        else:
            raise ValueError("Invalid account type")

    # Instance methods
    def print_customer(self):
        print("----- Customer Record -----")
        print(f"Name: {self.name}")
        print(f"Account number: {BankAccount.branch_number}-{BankAccount.__type_saving if self._type == 'saving' else BankAccount.__type_loan}-{self.account_number}")
        account_type_str = ''
        if self._type == 'saving':
            account_type_str = 'saving'
        elif self._type == 'loan':
            account_type_str = 'loan'
        print(f"Account type: {account_type_str}")
        print(f"Balance: {self.balance}")
        print("----- End Record -----\n")

    def deposit(self, amount=0):
        self.balance += amount
        return self.balance

    def pay_loan(self, amount=0):
        self.balance += amount
        return self.balance
    