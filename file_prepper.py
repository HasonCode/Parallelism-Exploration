import math
value_files = [open("calculated_values_thread_py.txt","r"), open("calculated_values_parallel_go.txt","r"),
               open("calculated_values_c.txt","r"),open("calculated_values_f08.txt","r"),open("calculated_values_go.txt","r"),
               open("calculated_values_py.txt","r"),open("calculated_values_parallel_c.txt","r"),open("calculated_values_parallel_f08.txt","r"),
               open("calculated_values_mp_py.txt","r")]
modified_value_files = [open("error_multithreaded_python.txt","w"),open("error_parallel_go.txt","w"), open("error_c.txt","w"),
                         open("error_f08.txt","w"),open("error_go.txt","w"),open("error_python.txt","w"),
                         open("error_parallel_c.txt","w"),open("error_parallel_f08.txt","w"),open("error_parallel_python.txt","w")]
len_file = 100

def file_prep(len_file,value_file,modified_value_file):
    for i in range(len_file):
        vals = value_file.readline().split(" ")
        while "" in vals:
            vals.remove("")
        if "\n" in vals:
            vals.remove('\n')
        modified_value_file.write(vals[0]+" "+str(abs(math.pi-float(vals[-1])))+" \n")

for i in range(len(value_files)):
    file_prep(len_file,value_files[i],modified_value_files[i])
    value_files[i].close()
    modified_value_files[i].close()

pi_vals = open("pi_values.txt","w")
counter = 1
for i in range(len_file):
    pi_vals.write(str(counter)+ " "+str(math.pi)+"\n")
    counter+=100000
