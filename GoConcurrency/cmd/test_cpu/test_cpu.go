package main

import (
	"concurrency/cpu"
	"concurrency/cpu/plot"
)

func main() {
	// Will run into an error
	results, error := cpu.RunTest("something else")

	if error != nil {
		println(error.Error())
	} else {
		plot.CreateAndSavePlot(results, "cpu_bound_scatter.png")
	}

	// Runs the test for CPU bound tasks
	results, error = cpu.RunTest("cpu")

	if error != nil {
		println(error.Error())
	} else {
		plot.CreateAndSavePlot(results, "cpu_bound_scatter.png")
	}

	// Runs the test for IO bound tasks
	results, error = cpu.RunTest("io")

	if error != nil {
		println(error.Error())
	}
	plot.CreateAndSavePlot(results, "io_bound_scatter.png")
}
