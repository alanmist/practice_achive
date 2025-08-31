import time

def  show_time(func):
    
    def wrapper(*args,**kwargs):
        star_time=time.time()
        result=func(*args, **kwargs)
        end_time=time.time()
        time_took= end_time - star_time
        print(f"Function took time {time_took:.6f}")
        return result
    return wrapper

@show_time
def slow_func():
    time.sleep(2)
    
slow_func()
