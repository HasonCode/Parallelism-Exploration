#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <omp.h>
#include <math.h>
double monte_carlo(int iterations){
    srand(time(NULL));
    double pi = 0, x = 0, y = 0;
    for (int i = 0; i<iterations; i++){
        y = rand()/2147483648.0;
        x = rand()/2147483648.0;
        if (sqrtf(y*y+x*x)<=1){
            pi++;
        }
    }
    return (pi/iterations)*4;
}

double monte_carlo_parallel(int iterations){
    double pi = 0, x = 0, y = 0, temp_sum;
    #pragma omp parallel shared(pi) private(x,y,temp_sum)
    {
        unsigned int random_seed = time(NULL) ^ omp_get_thread_num();
        temp_sum = 0;
        #pragma omp for
            for (int i = 0; i<iterations;i++){
                x = rand_r(&random_seed)/2147483648.0;
                y = rand_r(&random_seed)/2147483648.0;
                if (sqrtf(x*x+y*y)<1.0){
                    temp_sum++;
                }
            }
        #pragma omp critical
        {
            pi=pi+temp_sum;
        }
    }
    return pi/iterations*4;
}

/*539,432,212,129*/
void file_doer(){
    FILE *calculated_pointer;
    FILE *time_pointer;
    FILE *calculated_pointer2;
    FILE *time_pointer2;
    calculated_pointer = fopen("calculated_values_parallel_c.txt","w"); 
    time_pointer = fopen("time_values_parallel_c.txt","w");
    calculated_pointer2 = fopen("calculated_values_c.txt","w"); 
    time_pointer2 = fopen("time_values_c.txt","w");
    int iteration_cap = pow(10.0,7.0);
    double value_array[2];
    double time_array[2];
    double value_array2[2];
    double time_array2[2];
    struct timespec start,end;

    for (int i = 1; i<iteration_cap;i+=100000){
        value_array[0]=0;
        value_array[1]=0;
        time_array[0]=0;
        time_array[1]=0;
        value_array2[0]=0;
        value_array2[1]=0;
        time_array2[0]=0;
        time_array2[1]=0;
        for (int j = 0; j<100;j++){
            value_array[0] += i;
            clock_gettime(CLOCK_REALTIME,&start);
            value_array[1] += monte_carlo_parallel(i);
            time_array[0]+= i;
            clock_gettime(CLOCK_REALTIME,&end);
            time_array[1]+=(fabsf((double)(end.tv_nsec-start.tv_nsec)));

            value_array2[0] += i;
            clock_gettime(CLOCK_REALTIME,&start);
            value_array2[1] += monte_carlo(i);
            time_array2[0]+= i;
            clock_gettime(CLOCK_REALTIME,&end);
            time_array2[1]+=(fabsf((double)(end.tv_nsec-start.tv_nsec)));
        }
        value_array[0]/=100;
        value_array[1]/=100;
        value_array2[0]/=100;
        value_array2[1]/=100;
        time_array[0]/=100;
        time_array[1]/=100;
        time_array2[0]/=100;
        time_array2[1]/=100;
        fprintf(calculated_pointer,"%f %f\n",value_array[0],value_array[1]);
        fprintf(time_pointer,"%f %f\n",time_array[0],time_array[1]);
        fprintf(calculated_pointer2,"%f %f\n",value_array2[0],value_array2[1]);
        fprintf(time_pointer2,"%f %f\n",time_array2[0],time_array2[1]);
    }
    fclose(calculated_pointer);
    fclose(calculated_pointer2);
    fclose(time_pointer);
    fclose(time_pointer2);
}

int main(){
    FILE* multithreaded;
    multithreaded = fopen("multithreaded_c_time_file.txt","w");
    struct timespec start,end;
    int num_iterations = 1000000000;
    clock_gettime(CLOCK_REALTIME,&start);
    monte_carlo(num_iterations);
    clock_gettime(CLOCK_REALTIME,&end);
    double time_comp = fabsf((double)(end.tv_nsec-start.tv_nsec));
    for (int i = 1; i<101;i++){
        printf("%d/100\n",i);
        omp_set_num_threads(i);
        clock_gettime(CLOCK_REALTIME,&start);
        monte_carlo_parallel(num_iterations);
        clock_gettime(CLOCK_REALTIME,&end);
        fprintf(multithreaded,"%d %f\n",i,time_comp/fabsf((double)(end.tv_nsec-start.tv_nsec)));
    }
    return 0;
}