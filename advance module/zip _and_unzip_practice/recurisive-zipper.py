import shutil
import os

base=r'C:\Users\hswap\OneDrive\Desktop\python\actual code\advance module\zip _and_unzip_practice'

comp_file=os.path.join(base,'note')
output_base=os.path.join(base,'arcive')
format_style=input("Please choose a format:(zip/gztar)")
print(format_style)

shutil.make_archive(output_base,format_style,comp_file)
print('done')