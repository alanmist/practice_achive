import collections


book = open(r'C:\Users\hswap\OneDrive\Desktop\python\actual code\advance module\chaper1', 'r')
line = book.read()


chars_to_remove = set(',.!?;:"\'-_()[]{}')
cleaned_text = ''.join(char for char in line if char not in chars_to_remove)


words = cleaned_text.split()


stopwords = {'the', 'a', 'of', 'and', 'to', 'in', 'is', 'it', 'that', 'was'}


filtered_words = [word.lower() for word in words if word.lower() not in stopwords]


book.close()


word_count = collections.Counter(filtered_words)

print("Top 20 most common words:")
for word, count in word_count.most_common(20):
    print(f"{word}: {count}")

print("Total unique words:", len(word_count))