FUNCTION monte_carlo(iterations,seed) result(pi)
    implicit NONE
    INTEGER, INTENT(in) :: iterations
    INTEGER, INTENT(in) :: seed
    DOUBLE PRECISION :: pi
    REAL :: x
    REAL :: y
    REAL:: i
    pi = 0
    call srand(seed)
    do i=1,iterations
        x = rand(0)
        y = rand(0)
        if (sqrt(x**2+y**2)<1) then
            pi=pi+1
        end if 
    end do
    pi = pi/iterations*4
end FUNCTION monte_carlo

FUNCTION monte_carlo_parallel(iterations,seed,num_threads) RESULT(pi)
    USE OMP_LIB
    implicit NONE
    INTEGER, INTENT(in) :: iterations
    INTEGER, INTENT(in) :: seed,num_threads
    DOUBLE PRECISION :: pi
    INTEGER :: thing,overall_count,counter
    REAL :: leftover, div_iter,x,y
    call srand(seed)
    pi = 0
    call omp_set_num_threads(num_threads)
    !$OMP PARALLEL SHARED(pi) PRIVATE(thing,counter,x,y)
        thing = 0
        !$OMP DO 
        do counter=1,iterations
            x = rand(0)
            y = rand(0)
            if (sqrt(x**2+y**2)<1.0) then 
                thing = thing+ 1
            end if
        end do
        !$OMP END DO
        !$OMP CRITICAL
            pi = pi+ thing
        !$OMP END CRITICAL
    !$OMP END PARALLEL
    pi=pi/iterations*4
end FUNCTION monte_carlo_parallel
FUNCTION monte_carlo_tests()
    CHARACTER(len = *), PARAMETER :: OUTPUT_FILE = "calculated_values_parallel_f08.txt"
    CHARACTER(len = *), PARAMETER :: TIME_FILE = "time_values_parallel_f08.txt"
    CHARACTER(len = *), PARAMETER :: OUTPUT_FILE2 = "calculated_values_f08.txt"
    CHARACTER(len = *), PARAMETER :: TIME_FILE2 = "time_values_f08.txt"
    DOUBLE PRECISION, EXTERNAL :: monte_carlo
    DOUBLE PRECISION, EXTERNAL :: monte_carlo_parallel
    INTEGER :: mc,time,mc2,time2,i,pow_cap,step,rate,j
    INTEGER :: start, end,seed
    REAL :: timesum1,timesum2
    DOUBLE PRECISION :: carlosum1,carlosum2
    pow_cap = 10**7
    open(file = OUTPUT_FILE,action = "write",status = "replace", newunit = mc)
    open(file = TIME_FILE,action = "write",status = "replace", newunit = time)
    open(file = OUTPUT_FILE2,action = "write",status = "replace", newunit = mc2)
    open(file = TIME_FILE2,action = "write",status = "replace", newunit = time2)
    do i=1,pow_cap,100000
        carlosum1=0
        carlosum2=0
        timesum1=0
        timesum2=0
        do j=1,100,1
            call SYSTEM_CLOCK(start,rate)
            call SYSTEM_CLOCK(seed,rate)
            carlosum1=carlosum1+monte_carlo_parallel(i,12,seed)
            call SYSTEM_CLOCK(end,rate)
            timesum1=timesum1+REAL(end-start)*(10**9)/rate
            call SYSTEM_CLOCK(start,rate)
            call SYSTEM_CLOCK(seed,rate)
            carlosum2=carlosum2+monte_carlo(i,seed)
            call SYSTEM_CLOCK(end,rate)
            timesum2=timesum2+REAL(end-start)*(10**9)/rate
        end do
        write(mc,*) REAL(i), carlosum1/100
        write(time,*) REAL(i),timesum1/100
        write(mc2,*) REAL(i), carlosum2/100
        write(time2,*) REAL(i),timesum2/100
    end do
    close(mc)
    close(time)
end FUNCTION monte_carlo_tests
PROGRAM test_func
    USE OMP_LIB
    DOUBLE PRECISION, EXTERNAL :: monte_carlo
    DOUBLE PRECISION, EXTERNAL:: monte_carlo_parallel
    DOUBLE PRECISION :: waste_of_space
    CHARACTER (len = *), PARAMETER :: SPEEDUP_FILE = "multithreaded_fortran_speedup.txt"
    INTEGER :: mt,i,pow_cap,rate,start,end,base_val,seed,core_count
    insert_val = 10000000
    core_count = 100
    call SYSTEM_CLOCK(start,rate)
    call SYSTEM_CLOCK(seed,rate)
    waste_of_space = monte_carlo(insert_val,seed)
    call SYSTEM_CLOCK(end,rate)
    base_val = end-start
    open(file = SPEEDUP_FILE, action = "write", status = "replace",newunit = mt)
    do i=1, core_count, 1
        print *, i
        call SYSTEM_CLOCK(start,rate)
        call SYSTEM_CLOCK(seed,rate)
        waste_of_space = monte_carlo_parallel(insert_val,seed,i)
        call SYSTEM_CLOCK(end,rate)
        write(mt, *) REAL(i), base_val/REAL(end-start)
    end do
    close(mt)
    ! print *, monte_carlo_parallel(10000.0,6)
    ! call execute_command_line('gnuplot -p \ ')
END PROGRAM test_func
