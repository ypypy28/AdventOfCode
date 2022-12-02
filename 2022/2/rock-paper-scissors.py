from enum import Enum

class Result(Enum):
    LOSE = 0
    DRAW = 3
    WIN = 6

MY_TURN = {
    'X': 1,
    'Y': 2,
    'Z': 3,
}

def get_result(opponent: str, me: str) -> Result:
    match (opponent, me):
        case ('A', 'X') | ('B', 'Y') | ('C', 'Z'):
            return Result.DRAW
        case ('A', 'Y') | ('B', 'Z') | ('C', 'X'):
            return Result.WIN
        case ('A', 'Z') | ('B', 'X') | ('C', 'Y'):
            return Result.LOSE
        case _:
            raise NotImplemented

def get_round_score(lst: list[str, str]) -> int:
    return MY_TURN[lst[1]] + get_result(*lst).value



if __name__ == "__main__":
    my_score = 0
    with open('input.txt', 'r') as f:
        for line in f:
            my_score += get_round_score(line.split())

    print('ANSWER:',
          f'Part 1: {my_score}',
          sep='\n')

