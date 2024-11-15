package plot

import (
	"concurrency/cpu"
	"fmt"
	"log"

	"gonum.org/v1/plot"
	"gonum.org/v1/plot/plotter"
	"gonum.org/v1/plot/vg"
)

// IntegerTicks implements the plot.Ticker interface
type IntegerTicks struct{}

// Ticks returns Ticks in the specified range with a step size of 1.
func (IntegerTicks) Ticks(min, max float64) []plot.Tick {
	var ticks []plot.Tick
	for i := int(min); i <= int(max); i++ {
		ticks = append(ticks, plot.Tick{Value: float64(i), Label: fmt.Sprintf("%d", i)})
	}
	return ticks
}

func CreateAndSavePlot(points []cpu.TestExecutionResult, plotName string) {
	plotPoints := make(plotter.XYs, len(points))

	for i, point := range points {
		plotPoints[i].X = float64(point.Cores)
		plotPoints[i].Y = point.ExecutionTime
	}
	// Create a new plot
	p := plot.New()

	// Set plot title and axis labels
	p.Title.Text = "CPU bound performance per core"
	p.X.Label.Text = "Number of assigned cores"
	p.Y.Label.Text = "Time elapsed (seconds)"

	// Create a scatter plot from the (x, y) points
	scatter, err := plotter.NewScatter(plotPoints)
	if err != nil {
		log.Fatalf("Could not create scatter plot: %v", err)
	}

	// Add the scatter plot to the plot
	p.Add(scatter)
	p.X.Tick.Marker = IntegerTicks{}

	// Save the plot to a PNG file
	if err := p.Save(6*vg.Inch, 4*vg.Inch, plotName); err != nil {
		log.Fatalf("Could not save plot: %v", err)
	}
}
