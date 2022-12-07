import sys


INPUT_FILE = sys.argv[1] if len(sys.argv) > 1 else "input.txt"


class Item:
    def __init__(self, name, *, parent=None, size=None):
        self.name = name
        self.parent = parent
        if parent is not None:
            parent.add(self)
        self.size = size
        if size is None:
            self.children = {}

    def __len__(self):
        if self.size is not None:
            return self.size
        size = 0
        for child in self.children:
            size += len(self.children[child])
        return size

    def __contains__(self, filename):
        return filename in self.children

    def __getitem__(self, val):
        return self.children[val]

    def __lt__(self, other):
        return len(self) < len(other)

    def __str__(self):
        res = self.name
        parent = self.parent
        while parent is not None:
            res = f"{parent.name if parent.name != '/' else ''}/{res}"
            parent = parent.parent
        return f"{len(self)}\t{res}"

    def add(self, file):
        self.children[file.name] = file


root = Item('/')
directories = set((root,))

with open(INPUT_FILE, 'r') as f:
    working_dir = None
    for line in f:
        args = line.split()
        if args[0] == "$":
            if args[1] == "cd":
                if args[2] == "..":
                    working_dir = working_dir.parent
                elif args[2] == "/":
                    working_dir = root
                else:
                    working_dir = working_dir[args[2]]
            elif args[1] == "ls":
                continue
        elif args[0].isnumeric():
            if args[1] not in working_dir:
                file = Item(args[1], parent=working_dir, size=int(args[0]))
        elif args[0] == "dir":
            if args[1] not in working_dir:
                dir_ = Item(args[1], parent=working_dir)
                working_dir.add(dir_)
                directories.add(dir_)

sum_part1 = 0
for directory in sorted(directories):
    len_dir = len(directory)
    if len_dir <= 100000:
        sum_part1 += len_dir

print("ANSWER:",
      f"Part 1: {sum_part1}",
      f"Part 2:",
      sep='\n')

