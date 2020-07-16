import time

from internet_graph import InternetGraph, PageVertex
import file_reader


def compute_avg_time(f, trials):
    """Return the average runtime of a function after a given number of
       trials.
       
       Parameters:
       f(function): the function being benchmarked
       trials(int): the number of times the function is executed

       Returns: float: the average runtime in miliseconds

    """
    def time_function(f):
        '''Return the runtime of a function in miliseconds.'''
        start = time.time()
        f()
        end = time.time()
        return end - start
   # run the function 10 times 
    times = [
        time for time_function(f) in range(10)
    ]
    # calculate the average time
    return (sum(times) / trials)
