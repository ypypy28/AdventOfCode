package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
)

var INPUT_FILE string = "input.txt"

type Elf struct {
	id       int
	calories int
}

// If there was an argument while starting program, change INPUT_FILE name to it.
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

	elfMaxColories := &Elf{}
	elf := &Elf{id: 1, calories: 0}
	for scanner.Scan() {
		line := scanner.Text()
		if line == "" {
			if elf.calories > elfMaxColories.calories {
				elfMaxColories = elf
			}
			elf = &Elf{id: elf.id + 1, calories: 0}
		}

		cal, _ := strconv.Atoi(line)
		elf.calories += cal
	}
	if elf.calories > elfMaxColories.calories {
		elfMaxColories = elf
	}

	fmt.Printf("ANSWER\nPART 1: %d\n", elfMaxColories.calories)
	fmt.Printf("%#v\n", *elfMaxColories)

}
