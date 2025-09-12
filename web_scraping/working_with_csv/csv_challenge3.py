import csv
from pathlib import Path

BASE=Path(r"C:\Users\hswap\OneDrive\Desktop\python\actual code\web_scraping\working_with_csv")
csv_path=BASE/"humans.csv"

with open(csv_path, mode='w',newline='',encoding='utf-8') as f:
    write=csv.writer(f)
    write.writerows([
        ['subhrangshu','24','kolkata'],
        ['tam', '45','benaroash'],
        ['santanu','25','pandua'],
        ['kam','35','hooghly'],
        
    ])
with open(csv_path,encoding='utf-8')as f:
    reader=csv.reader(f)
    for row in reader:
        if int(row[1])>=25:
            print(row[1])
        
        
