def to_str(bytes_or_str):
    if isinstance(bytes_or_str,str):
        value=bytes_or_str.encode('utf-8')
    else:
        value=bytes_or_str
    return value

name=to_str(b'subhrangsu')
print(type(name))
