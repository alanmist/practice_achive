def add(a,b):
    return (a+b)


def subtract(a,b):
    return (a-b)


def multiply(a,b):
    return (a*b)


def divide(a,b):
    try:

        if b!=0:
            return (a/b)
        else:
            raise ValueError
    except ValueError:
        print("denominator is 0 you can divide anything with 0")
    

divide(2,5)
