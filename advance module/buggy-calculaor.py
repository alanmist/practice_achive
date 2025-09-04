import pdb
class Calculator():

    def __init__(self, *args):
        self.args=args
    

    def add(self):
        addition=0
        for number in self.args:
            #pdb.set_trace()
            addition +=number
        return addition
    def multiply(self):
        number=1
        for num in self.args:
            #pdb.set_trace()
            number *=num
        return number
    def devision(self):
        # Start with the first number
        if len(self.args) < 2:
            return self.args[0] if self.args else 0
            #pdb.set_trace()
        
        # Initialize result with the first number
        result = self.args[0]
        
        # Divide by each subsequent number
        for i in range(1, len(self.args)):
            #pdb.set_trace()
            result /= self.args[i]
        return result
        
    def subtraction(self):
        if len(self.args)<2:
            if self.args:
            
                return self.args[0]
            else:
                return 0
        result=self.args[0]
        for i in range(1,len(self.args)):
            #pdb.set_trace()
            result-=self.args[i]
            
        return result
    

cal=Calculator(4,2,3)

c=cal.subtraction()
print(c)

div1=Calculator(3,0)
div=div1.devision()
print(div)