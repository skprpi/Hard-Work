from curses import window
import pygame
from app.utils import *
from app.units import *
from enum import Enum
from typing import List, Tuple
from abc import ABC, abstractmethod
import os


class EventActions(Enum):
    QUITE=0
    KEEP=1
    CHANGE_SCENE=2

class Text:
    def __init__(self, text: str, size: int, color, window, X, Y):
        myfont = pygame.font.SysFont("Comic Sans MS", size)

        text_width, text_height = myfont.size(text)
        self.label = myfont.render(text, bool, color)
        self._window = window
        self.x = X - text_width // 2
        self.y = Y - text_height // 2
        self.color = color
        self.text = text

    def draw(self):
        self._window.blit(self.label, (self.x, self.y))

class Image:
    def __init__(self, X_c, Y_c, h, w, color, window):
        X = X_c - w // 2
        Y = Y_c - h // 2
        self.x = X
        self.y = Y
        self.h = h
        self.w = w
        self.color = color
        self.window = window

    def draw(self):
        pygame.draw.rect(self.window, self.color, [self.x, self.y, self.w, self.h])

class Button(Image):
    def __init__(self, X_c, Y_c, h, w, color, window):
        super().__init__(X_c, Y_c, h, w, color, window)

    def clicked(self, pos) -> bool:
        X, Y = pos
        return self.x <= X <= self.x + self.w and self.y <= Y <= self.y + self.h

class TextButton:
    def __init__(self, text: str, text_size: int, text_color, X_c, Y_c, h, w, button_color, window):
        self.button = Button(X_c, Y_c, h, w, button_color, window)
        self.text = Text(text, text_size, text_color, window, X_c, Y_c)

    def clicked(self, pos):
        return self.button.clicked(pos)

    def draw(self):
        self.button.draw()
        self.text.draw()

class Scene(ABC):
    def on_event(self, event: pygame.event.Event) -> EventActions:
        return EventActions.QUITE if event.type == pygame.QUIT else EventActions.KEEP, None

    @abstractmethod
    def update(self):
        pass


class PlayScene(Scene):
    def __init__(self, window, window_info):
        self.player = create_player(20, window)
        self.units_factory = UnitsFactory(self.player, window, window_info, 20)
        self.enemy_group = EnemyGroup()
        self.enemy_group.add(self.units_factory.create_random_unit())

        self._window = window
        self._window_info = window_info

        self.delta_create_unit_time = 500000000 # 0.5 sec
        self.start_time = time.time_ns()

        self.score = 1

    def on_event(self, event: pygame.event.Event):
        result = super().on_event(event)
        if result[0] != EventActions.KEEP:
            return result
        return EventActions.KEEP, None

    def update(self) -> None | Scene:
        if time.time_ns() - self.start_time > self.delta_create_unit_time:
            self.enemy_group.add(self.units_factory.create_random_unit())
            self.start_time = time.time_ns()
            self.score += 1
        self.player.draw()
        collide = pygame.sprite.spritecollide(self.player, self.enemy_group.get_sprite_unit_group(), False)
        self.enemy_group.draw_all()

        score_text = Text("Score: " + str(self.score), 30, ColorManager.BLACK.value, self._window, 70, 30)
        score_text.draw()

        if collide:
            return LooseScene(self._window, self._window_info) # Restart scene
        return None


class LooseScene(Scene):
    def __init__(self, window, window_info: WindowInfo):
        self._window = window
        self._window_info = window_info
        X, Y = window_info.get_screen_size()
        X = X // 2
        Y = Y // 2
        self.text_button = TextButton("Restart", 30, ColorManager.WHITE.value, X, Y, 150, 200, ColorManager.BLUE.value, window)

    def on_event(self, event: pygame.event.Event):
        result = super().on_event(event)
        if result[0] != EventActions.KEEP:
            return result
        
        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN and self.text_button.clicked(mouse_pos):
            return EventActions.CHANGE_SCENE, PlayScene(self._window, self._window_info) # Play Scene
        return EventActions.KEEP, None

    def update(self) -> None | Scene:
        self.text_button.draw()


class StartScene(Scene):
    def __init__(self, window, window_info: WindowInfo):
        self._window = window
        self._window_info = window_info
        X, Y = window_info.get_screen_size()
        X = X // 2
        Y = Y // 2
        self.text_button1 = TextButton("Start", 30, ColorManager.WHITE.value, X - 80, Y, 80, 150, ColorManager.BLUE.value, window)
        self.text_button2 = TextButton("Settings", 30, ColorManager.WHITE.value, X + 80, Y, 80, 150, ColorManager.BLUE.value, window)

    def on_event(self, event: pygame.event.Event):
        result = super().on_event(event)
        if result[0] != EventActions.KEEP:
            return result
        
        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN and self.text_button1.clicked(mouse_pos):
            return EventActions.CHANGE_SCENE, PlayScene(self._window, self._window_info) # Play Scene
        if event.type == pygame.MOUSEBUTTONDOWN and self.text_button2.clicked(mouse_pos):
            return EventActions.CHANGE_SCENE, InfoScene(self._window, self._window_info) # Play Scene
        return EventActions.KEEP, None

    def update(self) -> None | Scene:
        self.text_button1.draw()
        self.text_button2.draw()


class Icon:
    def __init__(self, X, Y, h, w, color, text: str, window):
        self.text = Text(text, 30, ColorManager.BLACK.value, window, X, Y + h // 2 + 30)
        self.button = Button(X, Y, h, w, color, window)

    def clicked(self, pos):
        return self.button.clicked(pos)

    def draw(self):
        self.button.draw()
        self.text.draw()


class SceneItem:
    def __init__(self, icon: Icon, description: str, env_name: str):
        self.icon = icon
        self.description = description
        self.env_name = env_name


class InfoScene(Scene):
    def __init__(self, window, window_info: WindowInfo):
        self._window = window
        self._window_info = window_info
        X, Y = window_info.get_screen_size()
        X = X // 2
        Y = Y // 2

        self.icons: List[SceneItem] = []
        self.icons.append(SceneItem(Icon(X - 200, Y, 100, 100, ColorManager.GREEN.value, "Zoombee", window), "Classic zombee unit will follow you during whole game", "zombee"))
        self.icons.append(SceneItem(Icon(X , Y, 100, 100, ColorManager.BLUE.value, "Smart zoombee", window), "Fast zombee may move faster than classick zombee", "smart_zombee"))
        self.icons.append(SceneItem(Icon(X + 200 , Y, 100, 100, ColorManager.BLACK.value, "Stopping zombee", window), "They are sleeping?", "sleeping_zombee"))
        self.back_button = TextButton("back", 30, ColorManager.WHITE.value, X, Y + 200, 80, 120, ColorManager.BLUE.value, window)

    def on_event(self, event: pygame.event.Event):
        result = super().on_event(event)
        if result[0] != EventActions.KEEP:
            return result
        mouse_pos = pygame.mouse.get_pos()
        for it in self.icons:
            el = it.icon
            if event.type == pygame.MOUSEBUTTONDOWN and el.clicked(mouse_pos):
                return EventActions.CHANGE_SCENE, SingleInfoScene(self._window, self._window_info, it.icon, it.description, it.env_name) # Play Scene
        
        if event.type == pygame.MOUSEBUTTONDOWN and self.back_button.clicked(mouse_pos):
            return EventActions.CHANGE_SCENE, StartScene(self._window, self._window_info)

        return EventActions.KEEP, None

    def update(self) -> None | Scene:
        for el in self.icons:
            el.icon.draw()
        self.back_button.draw()


class SingleInfoScene(Scene):
    def __init__(self, window, window_info: WindowInfo, icon: Icon, description: str, env_name: str):
        self._window = window
        self._window_info = window_info

        X, Y = window_info.get_screen_size()
        X = X // 2
        Y = Y // 2
        self.icon = Icon(X, 200, icon.button.h, icon.button.w, icon.button.color, icon.text.text, window)
        self.text = Text(description, 30, ColorManager.BLACK.value, window, X, Y + 30)
        self.button_on = TextButton("on unit", 30, ColorManager.WHITE.value, X - 100, Y + 200, 80, 120, ColorManager.GREEN.value, window)
        self.button_off = TextButton("off unit", 30, ColorManager.WHITE.value, X + 100, Y + 200, 80, 120, ColorManager.RED.value, window)
        self.env_name = env_name

    def on_event(self, event: pygame.event.Event):
        result = super().on_event(event)
        if result[0] != EventActions.KEEP:
            return result
        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN and self.button_on.clicked(mouse_pos):
            os.environ[self.env_name] = "on"
            return EventActions.CHANGE_SCENE, InfoScene(self._window, self._window_info)
        if event.type == pygame.MOUSEBUTTONDOWN and self.button_off.clicked(mouse_pos):
            os.environ[self.env_name] = "off"
            return EventActions.CHANGE_SCENE, InfoScene(self._window, self._window_info)
        
        return EventActions.KEEP, None

    def update(self) -> None | Scene:
        self.icon.draw()
        self.text.draw()
        self.button_off.draw()
        self.button_on.draw()

