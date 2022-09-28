from functools import wraps
import time


def time_record(func) :
    @wraps(func)
    def wrapper(*args, **kargs) :
        start = time.time()
        result = func(*args,**kargs)
        elapsed_time =  time.time() - start
        print(f'[{func.__name__}] {elapsed_time:.3f} sec for process')
        return result
    return wrapper
