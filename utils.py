# External imports
import numpy as np
import pygame

# Local imports
from config import (
    KM_PER_PX,
    SURFACE_SIZE_WIDTH,
    SURFACE_SIZE_HEIGHT
)


clock = pygame.time.Clock()

SPEED_MULTIPLIER = 1 # 1.01


def constrain_planet_to_screen(p_x, p_vx, p_y, p_vy):
    
    if real2px(p_x) >= SURFACE_SIZE_WIDTH:
        p_vx = -abs(p_vx) * SPEED_MULTIPLIER
    elif real2px(p_x) <= 0:
        p_vx = abs(p_vx) * SPEED_MULTIPLIER

    if real2px(p_y) >= SURFACE_SIZE_HEIGHT:
        p_vy = -abs(p_vy) * SPEED_MULTIPLIER  # negative means "go up"
    elif real2px(p_y) <= 0:
        p_vy = abs(p_vy) * SPEED_MULTIPLIER
    
    return p_x, p_vx, p_y, p_vy


def px2km(x):
    """ Screen lenghts to universe lengths """
    return x * KM_PER_PX


def real2px(x):
    """ Universe lengths to screen lengths """
    px = x * (1/KM_PER_PX)

    if isinstance(x, np.ndarray):
        return px.astype(np.int32)

    elif isinstance(x, float):
        return int(px)
    
    elif isinstance(x, int):
        return px
    
    else:
        raise Exception(f'{x}: {type(x)}')

def paused():
    """ Run an infinite loop until a mouse click is received """
    
    while True:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            return
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
                quit()

        pygame.display.update()
        clock.tick(15) 