# External imports
import numpy as np
import pygame

# Local imports
from config import KM_PER_PX


clock = pygame.time.Clock()

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

        pygame.display.update()
        clock.tick(15) 