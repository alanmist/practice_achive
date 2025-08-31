import os
import collections
import logging

 # or set an absolute path like r"C:\Users\...\Downloads"

EXT_MAP = {
    ".jpg": "images",
    ".jpeg": "images",
    ".png": "images",
    ".gif": "images",
    ".pdf": "documents",
    ".docx": "documents",
    ".doc": "documents",
    ".xls": "documents",
    ".xlsx": "documents",
    ".txt": "other",
    ".csv": "other",
    ".mp3": "music",
    }

DRY_RUN=False
LOG_LEVEL= logging.INFO

logging.basicConfig(level=LOG_LEVEL, format="%(levelname)s:%(message)s")

def get_path():
    while True:
        src=input("please provide a valid path that you want to scan: ")
        src=os.path.normpath(src)
        src=src.strip('"\'')

        if os.path.exists(src):
            return src
        else:
            print("invalid Path! please prvide a new one")

SRC=get_path()


def main():
        
    file_count=0
    error=0
    file_type=[]

    for root, subdirs, files in os.walk(SRC):
        print(f'This is the folder: {root}')
        print('\n')

        for sub in subdirs:
            print(f'found :{sub}')
        print('\n')

        for file in files:
            full_path=os.path.join(root,file)
            ext=os.path.splitext(file)[1].lower()
            
        
            target_dir=EXT_MAP.get(ext,'other')
            action="preview" if DRY_RUN else "scan"
            logging.info(f'{action}:{full_path} ->  {target_dir}')

        

            try:
                size=os.path.getsize(full_path)
                
                file_count +=1
                file_type.append(ext)

                if size> 1024*1024:
                    size_str=f"{size/(1024*1024):.1f}Mb"
                    
                elif size>1024:
                    size_str=f"{size/1024:.1f}Kb"
                    
                else:
                    size_str=f"{size}Bytes"
                    
                print(f'{file}: {size_str}')
            except Exception as e:
                error +=1
                logging.error(f'Failed to count: {file}' )
            
            
    print (f'File count: {file_count}') 
    if ext in EXT_MAP:
        sorting_list=collections.Counter(file_type)

    for filetype, numbers in sorting_list.items():
        print(f' {filetype}: {numbers} ')
       

    logging.info(f"Done. Count: {file_count}, Errors: {error}")

if __name__ == "__main__":
    main()
