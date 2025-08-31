def peek_next(iterable):
    for i in range(len(iterable)):
        try:
            peek=tuple([iterable[i],iterable[i+1]])
        except:
            peek=tuple([iterable[i],None])

        yield(peek)      


number=peek_next(list(range(10)))
for i in number:
    print(i)
num1=peek_next([])
for d in num1:
    print(d)