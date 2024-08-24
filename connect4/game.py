from collections import Counter
from dataclasses import dataclass
from enum import StrEnum
import random
import time

DEFAULT_FIELD_WIDTH = 6
DEFAULT_FIELD_HEIGHT = 7

SEQ_LEN = 4


class Balls(StrEnum):
    USER_1 = "X"
    USER_2 = "Y"


BallsMatrix = list[list[Balls]]


@dataclass
class Area:
    balls: BallsMatrix
    height: int
    width: int


class AreaDrawer:
    def __init__(self) -> None:
        self._was_drawn = False

    def redraw(self, area: Area):
        if self._was_drawn:
            remove_last_lines(area.height)

        for row in reversed(area.balls):
            output_row = []

            for ball in row:
                output_row.append(ball or "_")

            print("|".join(output_row))

        self._was_drawn = True


class FallingBalls:
    def __init__(
        self,
        field_width: int = DEFAULT_FIELD_WIDTH,
        field_height: int = DEFAULT_FIELD_HEIGHT,
    ) -> None:
        self.area = Area(
            balls=[[None for _ in range(field_width)] for _ in range(field_height)],
            height=field_height,
            width=field_width
        )
        self._balls_cnt = 0

    def add(self, ball: Balls, column: int):
        # todo: handle height overloading
        # todo: validate column
        highest_column = self.area.balls[-1]
        highest_column[column] = ball
        self._balls_cnt += 1

    def tick(self) -> bool:
        if not self._balls_cnt:
            return False

        has_shifts = False
        for row_i, row in enumerate(self.area.balls):
            if row_i == 0:
                continue

            for ball_i, ball in enumerate(row):
                if not ball:
                    continue
                row_below = self.area.balls[row_i - 1]
                has_empty_space_below = not bool(row_below[ball_i])

                if not has_empty_space_below:
                    continue
                row_below[ball_i] = ball
                row[ball_i] = None
                has_shifts = True
        return has_shifts



def find_winner(area: Area) -> Balls | None:
    # TODO: implement this
    return random.choice(list(Balls) + [None]*10)


def start():
    drawer = AreaDrawer()
    falling_balls = FallingBalls()
    next_ball_idx = 0

    while True:
        drawer.redraw(falling_balls.area)
        has_shifts = falling_balls.tick()

        if not has_shifts:
            winner = find_winner(falling_balls.area)
            if not winner:
                next_ball = list(Balls)[next_ball_idx]
                ball_column = int(input(f'Enter the column for {next_ball}: '))
                remove_last_lines(0)
                falling_balls.add(next_ball, ball_column)
                next_ball_idx = (next_ball_idx + 1) % len(Balls)
            else:
                print(f'Winner is {winner}')
                return
        time.sleep(1)


def remove_last_lines(num: int):
    print(f"\x1b[{num}A", end='\r')
