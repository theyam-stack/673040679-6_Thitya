from P2_bankaccount import BankAccount
# Creating an object
john = BankAccount('John', type='saving', balance=500)
tim = BankAccount('Tim', type='loan', balance=-1000000)
sarah = BankAccount('Sarah', type='saving')


# John asks to deposit 3,000 more and see the current balance.
# Tim wants to see the loan balance and he wants to pay half of the balance right away.
# Sarah wants to deposit 50,000,000
# Sarah wants to open another loan account for -100,000,000
print("---------------- Transactions ----------------")
john.deposit(3000)
print(f"\nJohn's current balance: {john.balance}")
print(f"\nTim's current balance: {tim.balance}")
tim.pay_loan(50000)
print(f"Tim's balance after paying half of the loan: {tim.balance}")
sarah.deposit(50000000)
print(f"\nSarah's current balance: {sarah.balance}")
sarah_loan = BankAccount('Sarah', type='loan', balance=-100000000)

# Using the methods
# Finally, show the account information of all accounts.
print()
john.print_customer()
tim.print_customer()
sarah.print_customer()