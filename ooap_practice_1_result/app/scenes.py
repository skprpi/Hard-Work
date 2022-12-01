import pygame
from abc import ABC, abstractmethod
from enum import Enum
import time
from core.units.view import RectangleUnitView
from app.units import Player, Zombee
from app.move import move_by_keyboard, get_target_mover
from app.collision import process_collisions
from app.utils import ColorManager


class EventActions(Enum):
    QUITE=0
    KEEP=1
    CHANGE_SCENE=2


class Scene(ABC):
    def on_event(self, event: pygame.event.Event) -> EventActions:
        return EventActions.QUITE if event.type == pygame.QUIT else EventActions.KEEP, None

    @abstractmethod
    def update(self):
        pass


class PlayScene(Scene):
    def create_player(self, window):
        view = RectangleUnitView((100, 100), 20, 20, ColorManager.RED.value, window)
        return Player(move_by_keyboard, view)

    def create_zombee(self, window, player):
        view = RectangleUnitView((200, 200), 20, 20, ColorManager.GREEN.value, window)
        return Zombee(get_target_mover(player, 5000000), view)

    def __init__(self, window, window_info):
        self.player = self.create_player(window)
        self.zombee = self.create_zombee(window, self.player)

        self._window = window
        self._window_info = window_info

        self.score = 1

    def on_event(self, event: pygame.event.Event):
        return EventActions.KEEP, None

    def update(self):
        # self.player, self.zombee = process_collisions([self.player, self.zombee])

        self.player, self.zombee = process_collisions([self.player, self.zombee])

        self.player.draw()
        self.zombee.draw()

        self.player.move(4)
        self.zombee.move(2)

