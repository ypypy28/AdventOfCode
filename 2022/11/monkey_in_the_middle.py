import operator
import sys
import typing
from heapq import nlargest


filename = sys.argv[1] if len(sys.argv) > 1 else "input.txt"


class Monkey:
    def __init__(
        self, starting_items: list[int],
        operation: typing.Callable,
        test: typing.Callable
    ) -> None:
        self.inspections = 0
        self.items = starting_items
        self.op = operation
        self.test = test

    def round(self, monkeys: list["Monkey"]) -> None:
        for item in self.items:
            self.inspections += 1
            item = self.op(item)
            item //= 3
            next_monkey_id = self.test(item)
            monkeys[next_monkey_id].receive(item)

        self.items.clear()

    def receive(self, item: int) -> None:
        self.items.append(item)

    def __repr__(self):
        return f"Monkey: {', '.join((str(it) for it in self.items))} inspections: {self.inspections}"


def read_monkey(file: typing.TextIO) -> list[str]:
    monkey = []
    while (line:=file.readline().strip()) not in ('\n', ''):
        monkey.append(line)
    return monkey


def parse_operation(example: str) -> typing.Callable:
    arg1, op, arg2 = example.partition('=')[2].split()

    match op:
        case '+':
            op = operator.add
        case '-':
            op = operator.sub
        case '*':
            op = operator.mul
        case _:
            raise NotImplementedError

    match arg1, arg2:
        case "old", "old":
            return lambda old: op(old, old)
        case "old", num:
            num = int(num)
            return lambda old: op(old, num)
        case _:
            raise ValueError(f"bad args {arg1=}, {arg2=} {example=}")


def parse_test(example: list[str]) -> typing.Callable:
    if "divisible" not in example[0]:
        raise NotImplementedError

    divisor, ok, not_ok = (int(line.rpartition(' ')[2]) for line in example)

    def test(val):
        return ok if val % divisor == 0 else not_ok
    return test


def create_monkey(monkey_data: list[str]):
    start_items = [int(it)
                   for it in (monkey_data[1]
                              .removeprefix('Starting items: ')
                              .split(', '))]
    operation = parse_operation(monkey_data[2].removeprefix("Operation: "))
    test = parse_test(monkey_data[3:6])

    return Monkey(start_items, operation, test)


def solve() -> int:
    monkeys = []
    with open(filename, 'r') as f:
        monkey_data = read_monkey(f)
        while len(monkey_data) == 6:
            monkeys.append(create_monkey(monkey_data))
            monkey_data = read_monkey(f)

    for _ in range(20):
        for monkey in monkeys:
            monkey.round(monkeys)

    two_largest = nlargest(2, monkeys, key=lambda m: m.inspections)
    return two_largest[0].inspections * two_largest[1].inspections


if __name__ == "__main__":
    part1 = solve()

    print("ANSWER:",
          f"Part 1: {part1}",
          sep='\n')
