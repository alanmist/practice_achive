import timeit

def even_word(sent):
    word = sent.split(' ')
    even = []
    for i in word:
        if len(i) % 2 == 0:
            even.append(i)
    return even

# For timing, use a fixed sentence
statment = """
even_word('This is a test sentence for timing')
"""
set_ups = """
from __main__ import even_word
"""
time_take = timeit.timeit(statment, set_ups, number=1000)
print(time_take)

# For user interaction
user_sent = input('Please provide a sentence: ')
print(even_word(user_sent))