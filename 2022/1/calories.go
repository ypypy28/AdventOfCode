package main

import (
	"bufio"
	"container/heap"
	"fmt"
	"os"
	"strconv"
	"strings"
)

var INPUT_FILE string = "input.txt"

type Elf struct {
	id       int
	calories int
}

type ElfHeap []*Elf

func (h ElfHeap) Len() int           { return len(h) }
func (h ElfHeap) Less(i, j int) bool { return h[i].calories < h[j].calories }
func (h ElfHeap) Swap(i, j int)      { h[i], h[j] = h[j], h[i] }
func (h *ElfHeap) Push(e any) {
	*h = append(*h, e.(*Elf))
}
func (h *ElfHeap) Pop() any {
	n := len(*h)
	poped := (*h)[n-1]
	*h = (*h)[0 : n-1]
	return poped
}

func (h ElfHeap) String() string {
	var sb strings.Builder
	sep := ""
	sb.WriteByte('[')
	for _, elfPointer := range h {
		sb.WriteString(fmt.Sprintf("%sElf(id=%d, calories=%d)", sep, elfPointer.id, elfPointer.calories))
		sep = ", "
	}
	sb.WriteByte(']')

	return sb.String()
}

// GetFilename changes INPUT_FILE If there was an argument while starting program.
func GetFilename() {
	if len(os.Args) > 1 {
		INPUT_FILE = os.Args[1]
	}
}

func main() {
	GetFilename()
	file, err := os.Open(INPUT_FILE)
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)

	elfs := &ElfHeap{}
	heap.Init(elfs)
	elf := &Elf{id: 1, calories: 0}
	heap.Push(elfs, elf)
	for scanner.Scan() {
		line := scanner.Text()
		if line == "" {
			heap.Push(elfs, elf)
			if len(*elfs) > 3 {
				heap.Pop(elfs)
			}
			elf = &Elf{id: elf.id + 1, calories: 0}
		}

		cal, _ := strconv.Atoi(line)
		elf.calories += cal
	}
	heap.Push(elfs, elf)
	heap.Pop(elfs)

	caloriesOfTop3Elfs := 0
	for i := range *elfs {
		caloriesOfTop3Elfs += (*elfs)[i].calories
	}

	fmt.Printf("ANSWER\nPart 1: %d\nPart 2: %d\n",
		(*elfs)[len(*elfs)-1].calories,
		caloriesOfTop3Elfs,
	)
	fmt.Printf("(%s)", elfs)

}
