package main
import("fmt")
import (
	"math"
	"math/rand/v2"
	"sync"
	"os"
	"time"
	"strconv"
)
func monte_carlo(iterations int64) float64{
	var x float64
	var y float64
	var pi float64 = 0
	for i:=int64(0); i<iterations; i++{
		x = rand.Float64()
		y = rand.Float64()
		if (math.Sqrt(x*x+y*y)<1){
			pi+=1
		}
	}
	return pi/float64(iterations)*4.0
}


func multi_thread_helper(iterations int64,wg *sync.WaitGroup, arr *[100000]float64, index int64,channel chan int){
	var x,y float64
	var pi float64
	pi=0
	for i:=int64(0);i<iterations;i++{
		x = rand.Float64()
		y = rand.Float64()
		if (math.Sqrt(x*x+y*y)<1){
			pi++
		}
	}
	arr[index]=pi
	defer wg.Done()
	return
}
func monte_carlo_multithread(iterations int64,num_threads int64) float64{
	channel := make(chan int,1)
	var wg sync.WaitGroup
	var leftover_threads int64 = iterations%num_threads
	var pi_final float64 = 0
	var value_array [100000]float64
	for i:=int64(0);i<num_threads;i++{
		wg.Add(1)
		if (i==0 && num_threads!=100000){
			go multi_thread_helper(leftover_threads,&wg,&value_array,i,channel)
		} else{
			go multi_thread_helper(iterations/num_threads,&wg,&value_array,i,channel)
		}
	}
	wg.Wait()
	for i := range value_array{
		if value_array[i]!=0{
			pi_final += float64(value_array[i])
		}
	}
	close(channel)
	return pi_final/float64(iterations)*4.0
}



func optional(){
	time_reg_val, err:= os.Create("time_values_go.txt")
	time_mp_val, err:= os.Create("time_values_parallel_go.txt")
	calc_reg_val, err:= os.Create("calculated_values_go.txt")
	calc_mp_val, err:= os.Create("calculated_values_parallel_go.txt")
	if err!=nil{
		panic(err)
	}
	var pow_cap int64 = int64(math.Pow(10,7))
	start:=time.Now()
	var time_since int64
	var timesum1,timesum2 int64
	var carlosum1,carlosum2 float64
	for i:=int64(1);i<pow_cap;i+=100000{
		timesum1=int64(0)
		timesum2=int64(0)
		carlosum1=0.0
		carlosum2=0.0
		for j:=0;j<100;j++{
			start=time.Now()
			carlosum1 +=monte_carlo(i)
			time_since = time.Since(start).Nanoseconds()
			timesum1+=time_since
			start=time.Now()
			carlosum2 += monte_carlo_multithread(i,10)
			time_since = time.Since(start).Nanoseconds()
			timesum2+=time_since
		}
		time_reg_val.WriteString(strconv.FormatInt(i,10)+" "+strconv.FormatInt(timesum1/int64(100),10)+"\n")
		calc_reg_val.WriteString(fmt.Sprint(strconv.FormatInt(i,10)+" ",carlosum1/float64(100))+"\n")
		time_mp_val.WriteString(strconv.FormatInt(i,10)+" "+strconv.FormatInt(timesum2/int64(100),10)+"\n")
		calc_mp_val.WriteString(fmt.Sprint(strconv.FormatInt(i,10)+" ",carlosum2/float64(100))+"\n")
	}
}
	// fmt.Println(monte_carlo_multithread(100000000))
	func main(){
		mt_time_file, err:= os.Create("mt_go_time.txt")
		if (err!=nil){
			panic(err)
		}
		var val_count,comp_val int64
		val_count = int64(1000000000)
		start := time.Now()
		monte_carlo(val_count)
		comp_val = time.Since(start).Nanoseconds()
		for i:=1;i<101;i++{
			fmt.Println(i)
			start = time.Now()
			monte_carlo_multithread(val_count,int64(i))
			mt_time_file.WriteString(fmt.Sprint(i)+" "+fmt.Sprint(float64(comp_val)/float64(time.Since(start).Nanoseconds()))+"\n")
		}
	}
