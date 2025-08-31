import os
import shutil
file_path = os.getcwd()
for root, sub_folders, files in os.walk(file_path):
    print(f'Subdirectories in {root}: {sub_folders}')
    print("\n")
    for sub in sub_folders:
        print(f'Subdirectory: {sub}')
        
    print('\n')
    for file in files:
        print(f'File: {file}')

        if file.endswith('.jpg'):
            full_path_jpg= os.path.join(root,file)
            print(f'JPG found:{full_path_jpg}')

            if os.path.exists(full_path_jpg):
                os.makedirs('C:\\Users\\hswap\\OneDrive\\Desktop\\python\\file mange\\new file\\imag',exist_ok=True)
                shutil.move(full_path_jpg,'C:\\Users\\hswap\\OneDrive\\Desktop\\python\\file mange\\new file\\imag')
                print('Transfer complete')
        if file.endswith('.pdf'):
            full_path_pdf= os.path.join(root,file)
            print(f'PDF found:{full_path_pdf}')

            if os.path.exists(full_path_pdf):
                os.makedirs('C:\\Users\\hswap\\OneDrive\\Desktop\\python\\file mange\\new file\\documen',exist_ok=True)
                shutil.move(full_path_pdf,'C:\\Users\\hswap\\OneDrive\\Desktop\\python\\file mange\\new file\\documen')
                print('Transfer complete')

        
        if file.endswith('.docx'):
            full_path_docx= os.path.join(root,file)
            print(f'PDF found:{full_path_docx}')

            if os.path.exists(full_path_docx):
                os.makedirs('C:\\Users\\hswap\\OneDrive\\Desktop\\python\\file mange\\new file\\documen',exist_ok=True)
                shutil.move(full_path_docx,'C:\\Users\\hswap\\OneDrive\\Desktop\\python\\file mange\\new file\\documen')
                print('Transfer complete')
                
        if file.endswith('.txt'):
            full_path_txt= os.path.join(root,file)
            print(f'PDF found:{full_path_txt}')

            if os.path.exists(full_path_txt):
                os.makedirs('C:\\Users\\hswap\\OneDrive\\Desktop\\python\\file mange\\new file\\other',exist_ok=True)
                shutil.move(full_path_txt,'C:\\Users\\hswap\\OneDrive\\Desktop\\python\\file mange\\new file\\other')
                print('Transfer complete')



        