import shutil

comp_folder=r'C:\Users\hswap\OneDrive\Desktop\python\actual code\advance module\zip _and_unzip_practice\note'

output_folder=r'C:\Users\hswap\OneDrive\Desktop\python\actual code\advance module\zip _and_unzip_practice\backup'

shutil.make_archive(output_folder,'zip',comp_folder)
zip_folder_path=r'C:\Users\hswap\OneDrive\Desktop\python\actual code\advance module\zip _and_unzip_practice\backup.zip'
output_folder2=r'C:\Users\hswap\OneDrive\Desktop\python\actual code\advance module\zip _and_unzip_practice\restore'
shutil.unpack_archive(zip_folder_path,output_folder2,'zip')