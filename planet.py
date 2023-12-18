# Standard-Library imports
import uuid

# External imports
import pygame
import numpy as np

# Local imports
from utils import real2px
from config import G


class Planet:
    def __init__(self, name, x, y, vx, vy, m, color, size=None):
        self.__id = f'{uuid.uuid4()}'
        self.name = name
        self.x = x     # km
        self.y = y     # km
        self.vx = vx   # km/s
        self.vy = vy   # km/s
        self.m = m     # kg
        self.color = color
        self.size = size
        self.counter = 0
        self.history = []
        print(f'Planet {name} created at {x, y}.')


    def draw(self, surface):        
        """ Draw the planet on the screen surface """
        
        width = 0 # Filled circle
        radius = 4
        if self.size is not None:
            radius = self.size
        
        pygame.draw.circle(
            surface,
            self.color,
            (real2px(self.x), real2px(self.y)),
            radius,
            width
        )


    def forces(self, planets):
        """
        Calculate the sum of forces on ths planet due to the other planets.

        Args:
            planets: A list of Planet objects.
        
        Returns:
            An array of shape (2,) with the total forces on the X and Y axis of
            the planet.
        """
        forces = []
        for p in planets:
            r = np.array([p.x - self.x, p.y - self.y])
            d = np.linalg.norm(r) * 1e3 # to meters
            r_unit = r/d # unit vector
            F = (r_unit * G * self.m * p.m + 1e-5) / (np.power(d, 2) + 1e-5) # Newtons
            forces.append(F)
        return np.sum(forces, axis=0) # Total sum of forces on each axis
    

    def get_acc(self, f):
        """Get acceleration of planet subjected to force `f`"""
        a = (f / self.m) * 1e-3  # multiply by 1e-3 to transform to km/s^2
        
        # # max/min acceleration
        # abs_acc = 4e-06
        # if a >= abs_acc:
        #     a = abs_acc
        # elif a <= -abs_acc:
        #     a = -abs_acc

        return a


    def get_state(self):
        return [self.x, self.vx, self.y, self.vy]


    def set_state(self, x):
        self.x, self.vx, self.y, self.vy = x


    def update_history(self, t):
        self.history.append((t, self.x, self.vx, self.y, self.vy))


    def __eq__(self, other) : 
        return self.__id == other.__id


    def __str__(self):
        """ Print the variables of interest of the planet """
        s = f'\n{self.name}\n' \
            f'Position: ({self.x:.2f}; {self.y:.2f})\n' \
            f'Velocity: ({self.vx:.4f}; {self.vy:.4f})'
        return s

