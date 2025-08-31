def range_clones(start,stop=None, step=1):
    
    if stop is None:
        stop=start
        start=0
    if step==0:
         raise ValueError("Step cannot be 0")
    
    
    current=start
    while (step> 0 and current<stop) or (step<0 and current> stop):
         current += step
         yield current
    
print(list(range_clones(5)))
print((list(range_clones(1,5))))
print(list(range_clones(5,0,-1)))