package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

const (
	TOTAL_DISK_SPACE = 70_000_000
	NEED_FREE_SPACE  = 30_000_000
)

var INPUT_FILE string = "input.txt"

func OpenInputFile() *os.File {
	if len(os.Args) > 1 {
		INPUT_FILE = os.Args[1]
	}
	file, err := os.Open(INPUT_FILE)
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
	return file
}

type Item interface {
	fmt.Stringer
	GetSize() int
}

type File struct {
	name   string
	parent *Directory
	size   int
}

func NewFile(name string, size int, parent *Directory) *File {
	return &File{
		name:   name,
		size:   size,
		parent: parent,
	}
}

func (f *File) GetSize() (size int) {
	return f.size
}

func (f *File) String() string {
	rev_path := make([]*string, 0)
	parent := f.parent
	if parent == nil {
		return "/" + f.name
	} else {
		for parent != nil {
			rev_path = append(rev_path, &parent.name)
			parent = parent.parent
		}
	}
	dirs := len(rev_path)
	sb := strings.Builder{}
	sb.WriteByte('/')
	for i := dirs - 2; i >= 0; i-- {
		sb.WriteString(*rev_path[i])
		sb.WriteByte('/')
	}
	sb.WriteString(f.name)
	return sb.String()
}

type Directory struct {
	name     string
	parent   *Directory
	children map[string]Item
}

func NewDir(name string, parent *Directory) *Directory {
	return &Directory{
		name:     name,
		parent:   parent,
		children: make(map[string]Item, 0),
	}
}

func (d *Directory) String() string {
	rev_path := make([]*string, 0)
	parent := d.parent
	if parent == nil {
		return d.name
	} else {
		for parent != nil {
			rev_path = append(rev_path, &parent.name)
			parent = parent.parent
		}
	}
	dirs := len(rev_path)
	sb := strings.Builder{}
	sb.WriteByte('/')
	for i := dirs - 2; i >= 0; i-- {
		sb.WriteString(*rev_path[i])
		sb.WriteByte('/')
	}
	sb.WriteString(d.name)
	return sb.String()
}

func (d *Directory) GetSize() (size int) {
	for _, child := range d.children {
		size += child.GetSize()
	}
	return
}

func main() {
	file := OpenInputFile()
	defer file.Close()

	scanner := bufio.NewScanner(file)
	root := NewDir("/", nil)

	directories := make([]*Directory, 0)
	directories = append(directories, root)

	workingDir := root

	for scanner.Scan() {
		line := scanner.Text()
		args := strings.Split(line, " ")
		if args[0] == "$" {
			if args[1] == "ls" {
				continue
			} else if args[1] == "cd" {
				if args[2] == ".." && workingDir.parent != nil {
					workingDir = workingDir.parent
				} else if args[2] == "/" {
					workingDir = root
				} else {
					workingDir = workingDir.children[args[2]].(*Directory)
				}
			}

		} else if args[0] == "dir" {
			_, ok := workingDir.children[args[1]]
			if ok {
				continue
			}
			newDir := NewDir(args[1], workingDir)
			workingDir.children[args[1]] = newDir
			directories = append(directories, newDir)
		} else {
			_, ok := workingDir.children[args[1]]
			if ok {
				continue
			}
			size, _ := strconv.Atoi(args[0])
			workingDir.children[args[1]] = NewFile(args[1], size, workingDir)
		}
	}

	unusedSpace := TOTAL_DISK_SPACE - root.GetSize()
	leftToFree := NEED_FREE_SPACE - unusedSpace
	dirToDelete := root
	dirToDeleteSize := dirToDelete.GetSize()
	sumPart1 := 0
	for _, dir := range directories {
		dirSize := dir.GetSize()
		if dirSize <= 100000 {
			sumPart1 += dirSize
		}
		if dirSize >= leftToFree && dirSize < dirToDeleteSize {
			dirToDelete = dir
			dirToDeleteSize = dirSize
		}
	}

	fmt.Printf("ANSWER:\nPart 1: %d\nPart 2: %d (rm %s)\n", sumPart1, dirToDeleteSize, dirToDelete)
}
