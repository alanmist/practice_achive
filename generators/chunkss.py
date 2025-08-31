
import itertools
def cunker(iterable, size):
    iters=[]
    iterables=iter(iterable)
    while True:


        iterable_product=list(itertools.islice(iterables,size))
        if not iterable_product:
            break
        iters.append(iterable_product)
    for i in iters:
        yield(i)

cunker("Ram sia ram",2)

