import time
import pygame
from typing import Tuple
from core.units.unit import Unit


def move_by_keyboard(position: Tuple[float, float], speed: int) -> Tuple[float, float]:
    presed_keys = pygame.key.get_pressed()
    X, Y = position
    X += (presed_keys[pygame.K_RIGHT] - presed_keys[pygame.K_LEFT]) * speed
    Y += (presed_keys[pygame.K_DOWN] - presed_keys[pygame.K_UP]) * speed
    return (X, Y)


def get_target_mover(target: Unit, target_update_position_time_ns: int):
    global start_time
    start_time = time.time_ns()
    def move_to_target(position: Tuple[float, float], speed: int) -> Tuple[float, float]:
        global start_time
        if time.time_ns() - start_time > target_update_position_time_ns:
            start_time = time.time_ns()
        X, Y = position
        X1, Y1 = target.get_position()
        X += (1 if (float)(X1 >= X) else -1) * speed
        Y += (1 if (float)(Y1 >= Y) else -1) * speed
        return (X, Y)
    return move_to_target
