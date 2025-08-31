def countdown(n):
    
    current=n
    
    while current>0:
        current= current-1
        yield current+1
    while current== 0:
        return ('Blast off')
e=countdown(3)
print(next(e))
print(next(e))
print(next(e))
print(next(e))