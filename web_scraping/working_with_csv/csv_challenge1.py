import csv


file_output=open(r"C:\Users\hswap\OneDrive\Desktop\python\actual code\web_scraping\working_with_csv\people.csv",mode='w',newline='')
csv_writer=csv.writer(file_output,delimiter=',')
csv_writer.writerow(['name','phone','city'])
csv_writer.writerows([['subhrangshu','23242323','kolkata'],['ram','64663425','aydha']])
file_output.close()

people_data=open(r"C:\Users\hswap\OneDrive\Desktop\python\actual code\web_scraping\working_with_csv\people.csv",encoding="utf-8")

csv_data=csv.reader(people_data)

data_line=list(csv_data)
people_data.close()
print(data_line)
for line in data_line:
    print(line)
    