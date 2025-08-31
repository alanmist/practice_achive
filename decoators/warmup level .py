import logging
def logger(func):
    
    def warps(*args,**kwargs):
        result=func(*args,**kwargs)
        print( f"Calling function name {func.__name__} output:{result} ")
        return result
    return warps
logging.basicConfig(level=logging.INFO)
@logger
def names(name="ram"):
    logging.info(f'function return name: {name}')
    return name
    
    
@logger
def greet():
    hi="Hello.how are you"
    logging.info(f'function greet you: {hi}')
    return hi


@ logger
def add(a,b):
    result=a+b
    logging.info(f'Function add and return: {result}')

    return result

@logger 
def multiply(a,b):
    result=a*b
    logging.info(f'fuction multiply and return: {result}')
    return result

print(names())
print(multiply(4,8))
print(add(7,9))
print(greet())