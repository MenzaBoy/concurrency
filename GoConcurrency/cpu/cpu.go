package cpu

import (
	"concurrency/cpu/tasks"
	"fmt"
	"math"
	"runtime"
	"sync"
	"time"
)

type CPUTestError struct {
	Code    int
	Message string
}

func (e *CPUTestError) Error() string {
	return fmt.Sprintf("Error %d: %s", e.Code, e.Message)
}

type TestExecutionResult struct {
	Cores         int
	ExecutionTime float64
}

func RunTest(taskToRun string) ([]TestExecutionResult, error) {
	if taskToRun != "cpu" && taskToRun != "io" {
		return nil, &CPUTestError{
			Code:    2,
			Message: "Unknown operation type.",
		}
	}
	testResults := []TestExecutionResult{}

	MaxNumberOfCores := runtime.NumCPU() // Sets the num of System cores

	for core := 1; core <= MaxNumberOfCores+5; core++ {
		// Creating a waitgroup, setting it to the numbers of processes and
		// limiting the number of usable CPUs by Go.
		wg := sync.WaitGroup{}
		wg.Add(MaxNumberOfCores)
		runtime.GOMAXPROCS(core)

		// Start measuring the time it takes the tests to run
		start := time.Now()

		// Spawn core number of tasks
		for i := 0; i < MaxNumberOfCores; i++ {

			if taskToRun == "cpu" {
				go tasks.CPUBlockingTask(&wg)
			} else {
				go tasks.IOBlockingTask(&wg)
			}
		}

		// Wait for all the tasks to finish
		wg.Wait()

		// Measure the elapsed time and save it in a slice
		elapsed := math.Round(time.Since(start).Seconds()*10) / 10
		testResults = append(testResults, TestExecutionResult{Cores: core, ExecutionTime: elapsed})
		println(fmt.Sprintf("Finished tasks with %d threads in %f seconds.", core, elapsed))
	}
	return testResults, nil
}
