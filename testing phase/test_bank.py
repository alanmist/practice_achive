import unittest
import bank

class Test_bank(unittest.TestCase):

    def test_deposit(self):
        deposit_test=bank.BankAccount('ram',1000)
        result=deposit_test.deposit(200)
        self.assertEqual(result,1200)
        
    
    def test_withdraw(self):
        withdraw_test=bank.BankAccount('ram',400)
        result=withdraw_test.withdraw(200)
        self.assertEqual(result,200)


    def test_negative_deposit(self):
        deposit_neg=bank.BankAccount('ram',1000)
        result=deposit_neg.deposit(-123)
        self.assertEqual(result,ValueError)


    def test_negative_withdraw(self):
        withdraw_neg=bank.BankAccount('ram',300)
        result=withdraw_neg.withdraw(-123)
        self.assertEqual(result,ValueError)

if __name__=='__main__':
    unittest.main()


