import random
import math
import multiprocessing
import concurrent.futures as cf
from time import process_time_ns

def monte_carlo(iterations:int) -> float:
    """Regular Monte Carlo, plotting iterations number of points randomly on a domain and range of
       [0,1) and returning the number within a circle of radius 0.5 centered at (0.5,0.5) divided by the 
       iteration count and multiplied by 4."""
    pi = 0.0
    for i in range(iterations):
        if (math.sqrt(random.random()**2+random.random()**2)<=1):pi+=1

    return pi/iterations*4

def multiprocessed_monte_carlo(iterations:int,num_processes:int) -> float:
    """Multiprocessed Monte Carlo, plotting iterations number of points randomly on a domain and range of
       [0,1) and returning the number within a circle of radius 0.5 centered at (0.5,0.5) divided by the 
       iteration count and multiplied by 4."""
    
    task_manager = multiprocessing.Pool(num_processes)
    input_arr = [iterations//num_processes for i in range(num_processes)]
    input_arr[0]+=iterations%num_processes
    while 0 in input_arr:
        input_arr.remove(0)
    output_arr = list(task_manager.map(monte_carlo,input_arr))
    return sum(output_arr)/len(output_arr)
#539,432,212,129

def multithreaded_monte_carlo(iterations:int,num_processes:int) -> float:
    """Multithreaded Monte Carlo, plotting iterations number of points randomly on a domain and range of
       [0,1) and returning the number within a circle of radius 0.5 centered at (0.5,0.5) divided by the 
       iteration count and multiplied by 4."""
    manager = cf.ThreadPoolExecutor(max_workers = num_processes)
    input_arr = [iterations//num_processes for i in range(num_processes)]
    input_arr[0]+=iterations%num_processes
    while 0 in input_arr:
        input_arr.remove(0)
    output_arr = list(manager.map(monte_carlo,input_arr))
    return sum(output_arr)/len(output_arr)
#The Fun Part

def base_trial_code():
    if __name__ == "__main__":
        calc_file = open("calculated_values_py.txt","w")
        time_file = open("time_values_py.txt","w")
        calc_file_mp = open("calculated_values_mp_py.txt","w")
        time_file_mp = open("time_values_mp_py.txt","w")
        calc_file_thread = open("calculated_values_thread_py.txt","w")
        time_file_thread = open("time_values_thread_py.txt","w")
        iterations = 10**7
        for i in range(1,iterations,100000):
            timesum1,timesum2,timesum3=0,0,0
            carlosum1,carlosum2,carlosum3=0,0,0
            for j in range(100):
                start = process_time_ns()
                carlosum1+=monte_carlo(i)
                timesum1+=process_time_ns()-start
                start = process_time_ns()
                carlosum2+=multiprocessed_monte_carlo(i)
                timesum2+=process_time_ns()-start
                start = process_time_ns()
                carlosum3+=multithreaded_monte_carlo(i)
                timesum3+=process_time_ns()-start
            calc_file.write(str(i)+"   "+str(carlosum1/100)+"\n")
            time_file.write(str(i)+"   "+str(timesum1/100)+"\n")
            calc_file_mp.write(str(i)+"   "+str(carlosum2/100)+"\n")
            time_file_mp.write(str(i)+"   "+str(timesum2/100)+"\n")
            calc_file_thread.write(str(i)+"   "+str(carlosum3/100)+"\n")
            time_file_thread.write(str(i)+"   "+str(timesum3/100)+"\n")
        calc_file.close()
        time_file.close()
        calc_file_mp.close()
        time_file_mp.close()
        calc_file_thread.close()
        time_file_thread.close()


if __name__ == "__main__":
    test_vals = 10000000
    start = process_time_ns()
    comp_point = monte_carlo(test_vals)
    time_point = process_time_ns() - start
    mp_time_file = open("mp_time_file.txt","w")
    mt_time_file = open("mt_time_file.txt","w")
    for i in range(1,101,1):
        print(f"{i}%")
        start = process_time_ns()
        val = multiprocessed_monte_carlo(test_vals,i)
        mp_time_file.write(str(i)+" "+str(time_point/(process_time_ns()-start))+"\n")
        start = process_time_ns()
        val = multithreaded_monte_carlo(test_vals,i)
        mt_time_file.write(str(i)+" "+str(time_point/(process_time_ns()-start))+"\n")
    mp_time_file.close()
    mt_time_file.close()
        