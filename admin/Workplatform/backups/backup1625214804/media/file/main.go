package main
 
import "fmt"
 

func main()  {
	s := "hello文剑华"
	var count int = 0

	for _,i := range s{
		fmt.Println(string(i))
		if len(string(i)) >=3{
			count++
		}
	
	}
	fmt.Println(count)
}