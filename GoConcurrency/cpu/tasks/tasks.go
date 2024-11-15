package tasks

import (
	"sync"
	"time"
)

func CPUBlockingTask(wg *sync.WaitGroup) {
	f := false
	for i := 0; i < 6_000_000_000; i++ {
		f = !f
	}
	wg.Done()
}

func IOBlockingTask(wg *sync.WaitGroup) {
	time.Sleep(1 * time.Second)
	wg.Done()
}
