import sys


filename = sys.argv[1] if len(sys.argv) > 1 else "input.txt"


class Register:
    def __init__(self, ths):
        self.val = 1
        self.cycle = 1
        self._ths = ths
        self._part1 = {}

    def process(self, command):
        match command.split():
            case "noop",:
                self.noop()
            case "addx", num:
                self.addx(int(num))
            case _:
                print(command)
                raise NotImplemented

    def cycle_inc(self):
        check_i = len(self._part1)-len(self._ths)
        if check_i < 1:
            check_cycle = self._ths[check_i]
            if self.cycle == check_cycle:
                self._part1[check_cycle] = self.strenth()
        self.cycle += 1

    def noop(self):
        self.cycle_inc()

    def addx(self, val):
        self.cycle_inc()
        self.cycle_inc()
        self.val += val

    def strenth(self):
        return self.cycle * self.val


V = Register((20, 60, 100, 140, 180, 220))
with open(filename, 'r') as f:
    for line in f:
        V.process(line.rstrip())

print("ANSWER",
      f"Part 1: {sum(V._part1.values())}",
      sep='\n')
