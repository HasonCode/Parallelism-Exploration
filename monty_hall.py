import random
from matplotlib import pyplot as plt
import math
def monty_hall_simulation(switching:bool)->int:
    """Simulates the Monty Hall problem, choosing a random door and returning if it is the prize door
    if switching is false, otherwise switching after a door is opened if switching is true."""
    inputs = [0,0,1]
    actual_values=[]
    for i in range(3):
        pull_val = random.choice(inputs)
        inputs.remove(pull_val)
        actual_values.append(pull_val)
    choice = random.randrange(0,3)
    if switching:
        zero_inds = []
        for i in range(len(actual_values)):
            if i != choice and actual_values[i]==0:
                if i<choice:
                    choice-=1
                actual_values.pop(i)
                break
        choice = 1-choice
    return actual_values[choice]


# for i in range(100):print(monty_hall_simulation(True))
def monty_hall_tester(iterations:int)->list:
    """Simulates iterations count of Monty Hall games in both cases of switching and non switching"""
    switch_sum, static_sum = 0,0
    for i in range(iterations):
        switch_sum+=monty_hall_simulation(True)
        static_sum+=monty_hall_simulation(False)
    return switch_sum/iterations,static_sum/iterations

def monty_hall_data_collection(min_iterations:int,max_iterations:int,power:int)->list:
    """Processes iterations of Monty Hall into lists of data, starting inclusively at min_iterations and
    exclusively going to max_iterations, increasing by step"""
    switch_vals, static_vals, iteration_counts = [],[],[]
    i = min_iterations
    while i<=max_iterations:
        print(f"{(i/max_iterations)*100}%")
        switch_sum,static_sum = monty_hall_tester(i)
        switch_vals.append(switch_sum)
        static_vals.append(static_sum)
        iteration_counts.append(i)
        i = i*power
    return switch_vals,static_vals,iteration_counts



def monty_hall_plotter(start:int,stop:int,power:int):
    """Plots Monty Hall iterations starting inclusively at start and exclusively going to stop, increasing
    by step"""
    switch_vals,static_vals,iteration_counts = monty_hall_data_collection(start,stop,power)
    plt.xscale("log")
    line1, = plt.plot(iteration_counts,switch_vals,"ob-",label = "With Switching")
    line2, = plt.plot(iteration_counts,static_vals,"^g-",label = "Without Switching")
    line3, = plt.plot(iteration_counts,[1/3 for i in range(len(iteration_counts))],",k:",label = "1/3")
    line4, = plt.plot(iteration_counts,[2/3 for i in range(len(iteration_counts))],",k:",label="2/3")
    plt.title("Monty Hall Problem")
    plt.xlabel("Iterations")
    plt.ylabel("Fraction Right")
    plt.legend(handles = [line1,line2,line3,line4])
    plt.savefig("monty_hall_problem")

monty_hall_plotter(1,2000000,2)
    
    