from typing import Tuple
import pygame

from app.utils import ColorManager, WindowInfo
from app.scenes import *

window_info = WindowInfo(60, 800, 600)

pygame.init()
pygame.mixer.init()
window = pygame.display.set_mode(window_info.get_screen_size())
pygame.display.set_caption("Just run")
clock = pygame.time.Clock()

curr_scene = PlayScene(window, window_info)

running = True
while running:
    clock.tick(window_info.get_fps())
    for event in pygame.event.get():
        status, new_scene = curr_scene.on_event(event)
        if status == EventActions.QUITE:
            running = False
        elif status == EventActions.CHANGE_SCENE:
            curr_scene = new_scene

    window.fill(ColorManager.WHITE.value)

    new_scene = curr_scene.update()
    if new_scene:
        curr_scene = new_scene

    pygame.display.flip()
pygame.quit()
