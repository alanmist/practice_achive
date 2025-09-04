import timeit


number1=[x**2 for x in range(10_000)]

stmt="""
[x**2 for x in range(10_000)]
"""
setup=""
 
time=timeit.timeit(stmt,setup,number=100000)

print(time)




number2=list(map(lambda x: x**2, range(10_000)))



