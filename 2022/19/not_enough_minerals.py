import sys
from collections import namedtuple


FILENAME = sys.argv[1] if len(sys.argv) > 1 else "test_input.txt"
Blueprint = namedtuple("Blueprint", "ore_bot clay_bot obsidian_bot geode_bot")
Resources = namedtuple("Resources", "ore clay obsidian geode")
MINUTES = 24


class BlueprintsIterator:
    def __init__(self, filename: str):
        self.filename = filename

    def __iter__(self):
        self.__f = open(self.filename, 'r')
        return self

    def __next__(self):
        if self.__f.closed:
            raise StopIteration

        line = self.__f.readline()
        if line == '':
            self.__f.close()
            raise StopIteration

        robots_cost = line.split('. ')
        ore_robot = Resources(int(robots_cost[0].split(' ')[-2]), 0, 0, 0)
        clay_robot = Resources(int(robots_cost[1].split(' ')[-2]), 0, 0, 0)
        obsidian_robot = Resources(*(int(robots_cost[2].split(' ')[i])
                                     for i in (-5, -2)),
                                     0, 0)
        geode_ore, geode_obsidian = (int(robots_cost[3].split(' ')[i]) for i in (-5, -2))
        geode_robot = Resources(geode_ore, 0, geode_obsidian, 0)

        return Blueprint(ore_robot, clay_robot, obsidian_robot, geode_robot)


class Factory:
    def __init__(self, blueprint: Blueprint):
        for field in Resources._fields:
            setattr(self, field, 0)
        self.bots = {Resources._fields[0]: 1}
        self.bot_costs = {bot_type: resources
                          for bot_type, resources in zip(Resources._fields, blueprint)}
        self._minute = 0

    def _can_build(self, bot_type) -> None:
        # print(f"{bot_type=}: {self.bot_costs[bot_type]=}")
        return all(getattr(self, field) >= getattr(self.bot_costs[bot_type], field)
                   for field in Resources._fields)

    def round(self):
        self._minute += 1
        print(f"\n== Minute {self._minute} == "
              f"(ore={self.ore} "
              F"clay={self.clay} "
              f"obsidian={self.obsidian} "
              f"geodes={self.geode})")
        new_bots = {bot_type: 0 for bot_type in Resources._fields}
        for field in reversed(Resources._fields):
            # print(f"{field}-robot can build? {self._can_build(field)=}")
            if self._can_build(field):
                new_bots[field] += 1
                spend = []
                for resource, value in zip(
                    self.bot_costs[field]._fields,
                    self.bot_costs[field]
                ):
                    if value != 0:
                        setattr(self, resource, getattr(self, resource) - value)
                        spend.append((value, resource))

                spended = ' and '.join(f"{value} {resource}" for value, resource in spend)
                print(f"Spend {spended} "
                    f"to start building a {field}-collecting robot.")
                break


        for resource in self.bots:
            setattr(self, resource, getattr(self, resource, 0) + self.bots[resource])
            print(f"{self.bots[resource]} {resource}-collecting robot collects "
                  f"{self.bots[resource]} {resource}; "
                  f"you now have {getattr(self, resource)} {resource}.")

        for bot_type in new_bots:
            if new_bots[bot_type] != 0:
                self.bots[bot_type] = self.bots.get(bot_type, 0) + new_bots[bot_type]
                print(f"{new_bots[bot_type]} new {bot_type}-collecting robot is ready; "
                      f"you now have {self.bots[bot_type]} of them.")



def solve(filename: str) -> tuple[int, int]:

    quality_levels = []

    for i, bp in enumerate(BlueprintsIterator(filename), start=1):
        factory = Factory(bp)

        for _ in range(MINUTES):
            factory.round()

        quality_levels.append(factory.geode * i)

        print(f"BLUEPRINT {i}: {factory.geode=}\n\n")


    return sum(quality_levels), 0


if __name__ == "__main__":
    part1, part2 = solve(FILENAME)

    print("ANSWER:",
          f"Part 1: {part1}",
          f"Part 2: {part2}",
          sep='\n')


