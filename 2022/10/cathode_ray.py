import sys


filename = sys.argv[1] if len(sys.argv) > 1 else "input.txt"


class Register:
    def __init__(self, ths):
        self.val = 1
        self.cycle = 1
        self._ths = ths
        self._part1 = {}
        self.sprite_size = 3
        self.crt_width = 40

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
        self.produce_pixel()
        if self.cycle in self._ths:
            self._part1[self.cycle] = self.strenth()
        self.cycle += 1

    def noop(self):
        self.cycle_inc()

    def addx(self, val):
        self.cycle_inc()
        self.cycle_inc()
        self.val += val

    def strenth(self):
        return self.cycle * self.val

    def produce_pixel(self):
        x = (self.cycle-1) % self.crt_width
        draw_sign = '#' if abs(self.val-x) < self.sprite_size-1 else '.'
        sys.stdout.write(draw_sign)
        sys.stdout.flush()
        if x == self.crt_width-1:
            sys.stdout.write('\n')


V = Register((20, 60, 100, 140, 180, 220))
with open(filename, 'r') as f:
    for line in f:
        V.process(line.rstrip())

print("\nANSWER",
      f"Part 1: {sum(V._part1.values())}",
      sep='\n')
