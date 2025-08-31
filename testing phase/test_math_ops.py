'''file importing'''
import unittest
import Math_ops

class TesingMath (unittest.TestCase):
    '''this is the start of acctual testing'''


    def test_add(self):
        """testing adds function"""
        result=Math_ops.add(3,7)
        self.assertEqual(result,10)


    def test_subtract(self):
        """testing subtract function"""
        result=Math_ops.subtract(6,3)
        self.assertEqual(result,3)


    def test_multiply(self):
        """testing multiply function"""
        result=Math_ops.multiply(9,7)
        self.assertEqual(result,63)


    def test_divide(self):
        """testing didvide function"""
        result=Math_ops.divide(60,15)
        self.assertEqual(result,4)


if __name__=="__main__":
    unittest.main()
