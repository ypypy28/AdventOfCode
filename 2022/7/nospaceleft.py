import sys


INPUT_FILE = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
TOTAL_DISK_SPACE = 70_000_000
NEED_FREE_SPACE = 30_000_000


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
        return res

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

unused_space = TOTAL_DISK_SPACE - len(root)
left_to_free = NEED_FREE_SPACE - unused_space
dir_to_delete = root
sum_part1 = 0
for directory in directories:
    len_dir = len(directory)
    if len_dir <= 100000:
        sum_part1 += len_dir
    if left_to_free <= len_dir < len(dir_to_delete):
        dir_to_delete = directory


print(f"{unused_space=}\n{left_to_free=}, ")

print("ANSWER:",
      f"Part 1: {sum_part1}",
      f"Part 2: {len(dir_to_delete)} ({dir_to_delete})",
      sep='\n')

