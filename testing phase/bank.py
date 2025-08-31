class BankAccount():


    def __init__(self,name,balance):
        self.name = name
        self.balance = balance


    def deposit(self,amount):
        
        if amount>0:
            self.balance += amount
            return self.balance
        else:
            raise ValueError
           

    def withdraw(self,amount):

        if amount>0:
            self.balance -= amount
            return self.balance
        else:
            print('fuck you')
