from enum import Enum


class Result(Enum):
    LOSE = 0
    DRAW = 3
    WIN = 6


MY_TURN = {
    "PART 1": {
        'X': 1,
        'Y': 2,
        'Z': 3,
    },
    "PART 2": {
        'A': 1,
        'B': 2,
        'C': 3,
    },
}

RESULT_PART2 = {
    'X': Result.LOSE,
    'Y': Result.DRAW,
    'Z': Result.WIN,
}

STRATEGIES = {
    Result.LOSE: {'A': 'C', 'B': 'A', 'C': 'B'},
    Result.DRAW: {'A': 'A', 'B': 'B', 'C': 'C'},
    Result.WIN:  {'A': 'B', 'B': 'C', 'C': 'A'},
}


def get_result_part1(opponent: str, me: str) -> Result:
    match (opponent, me):
        case ('A', 'X') | ('B', 'Y') | ('C', 'Z'):
            return Result.DRAW
        case ('A', 'Y') | ('B', 'Z') | ('C', 'X'):
            return Result.WIN
        case ('A', 'Z') | ('B', 'X') | ('C', 'Y'):
            return Result.LOSE
        case _:
            raise NotImplementedError


def get_my_shape_score_part2(opponent: str, result: str) -> int:
    my_shape = STRATEGIES[RESULT_PART2[result]][opponent]
    return MY_TURN["PART 2"][my_shape]


def get_round_score(lst: list[str]) -> tuple[int, int]:
    return (MY_TURN["PART 1"][lst[1]] + get_result_part1(*lst).value,
            get_my_shape_score_part2(*lst) + RESULT_PART2[lst[1]].value)


if __name__ == "__main__":
    my_score1 = my_score2 = 0
    with open('input.txt', 'r') as f:
        for line in f:
            score_part1, score_part2 = get_round_score(line.split())
            my_score1 += score_part1
            my_score2 += score_part2

    print('ANSWER:',
          f'Part 1: {my_score1}',
          f'Part 2: {my_score2}',
          sep='\n')
