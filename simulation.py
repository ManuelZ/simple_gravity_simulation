# Built-in imports
import time
from math import sqrt
from math import atan2
from math import cos
from math import sin

# External imports
import pygame
import numpy as np
from scipy.integrate import solve_ivp
from scipy.spatial.distance import euclidean

# Local imports
from utils import px2km
from utils import real2px
from utils import paused
from config import G
from config import EARTH_MASS
from config import MARS_MASS
from config import X_MASS
from config import SURFACE_SIZE
from config import EARTH_MARS_DISTANCE
from config import INITIAL_VELOCITY
from config import COLORS


# Total number of seconds to simulat3
t_sim = 50 * 365 * 24 * 3600 # seconds

# Time chunks to give to the solver
resolution = 1/(3600*24) # days

t = np.linspace(0, t_sim, int(t_sim * resolution + 1))

def model(t, X, p1, p2, p3):
    """
    Refer to https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_ivp.html
    """
    # Extract variables
    xearth, xdotearth, yearth, ydotearth = X[:4]
    xmars, xdotmars, ymars, ydotmars     = X[4:8]
    x3, xdot3, y3, ydot3                 = X[8:]

    # Calculate forces on each planet
    Fxearth, Fyearth = p1.forces([p2, p3])
    Fxmars, Fymars   = p2.forces([p1, p3])
    Fx3, Fy3         = p3.forces([p1, p2])

    # Define the new derivative vector
    Xdot = [
        xdotearth,
        (Fxearth/p1.m) * 1e-3, # multiply by 1e-3 to transform to km
        ydotearth,
        (Fyearth/p1.m) * 1e-3, # multiply by 1e-3 to transform to km
        
        xdotmars,
        (Fxmars/p2.m) * 1e-3, # multiply by 1e-3 to transform to km
        ydotmars,
        (Fymars/p2.m) * 1e-3, # multiply by 1e-3 to transform to km

        xdot3,
        (Fx3/p3.m) * 1e-3, # multiply by 1e-3 to transform to km
        ydot3,
        (Fy3/p3.m) * 1e-3 # multiply by 1e-3 to transform to km
    ]
    
    return Xdot


class Planet:
    def __init__(self, name, x, y, vx, vy, m, color):
        self.name = name
        self.x = x     # km
        self.y = y     # km
        self.vx = vx   # km/s
        self.vy = vy   # km/s
        self.m = m     # kg
        self.color = color
        self.last_state = x,vx,y,vy
        self.counter = 0
        print(f'Planet {name} created at {x, y}.')


    def draw(self, surface):        
        """ Draw the planet on the screen surface """
        
        width = 0 # Filled circle
        radius = 8
        pygame.draw.circle(
            surface,
            self.color,
            (real2px(self.x), real2px(self.y)),
            radius,
            width
        )


    def forces(self, planets):
        """
        Calculate the sum of forces on ths planet du to the other given planets

        Args:
            planets: A list of Planet objects
        
        Returns:
            A (2,) array with the total forces on the X and Y axis of the planet
        """
        forces = []
        for p in planets:
            r = np.array([p.x - self.x, p.y - self.y])
            d = np.linalg.norm(r) * 1e3 # to meters
            r_unit = r/d # unit vector
            F = (r_unit * G * self.m * p.m) / np.power(d, 2) # Newtons
            forces.append(F)
        return np.sum(forces, axis=0)
    

    def get_state(self):
        return [self.x, self.vx, self.y, self.vy]

    def set_state(self, x):
        self.x, self.vx, self.y, self.vy = x

    def __str__(self):
        """ Print the variables of interest of the planet """
        s = f'\n{self.name}\n' \
            f'Position: ({self.x:.1f}; {self.y:.1f})\n' \
            f'Velocity: ({self.vx:.2f}; {self.vy:.2f})'
        return s


def main():
    """ Set up the game and run the main game loop """
    
    ###########################################################################
    # PYGAME SETUP
    ###########################################################################

    pygame.init()
    pygame.font.init()
    pygame.display.set_caption('Gravity simulation')

    # Create surface of (width, height)
    main_surface = pygame.display.set_mode((SURFACE_SIZE+20, SURFACE_SIZE+20))


    ###########################################################################
    # DEFINE PLANETS
    ###########################################################################
    p1 = Planet(
        'Earth',
        x=px2km(SURFACE_SIZE/3),
        y=px2km(SURFACE_SIZE/3),
        vx=INITIAL_VELOCITY,
        vy=0,
        m=EARTH_MASS,
        color=COLORS['blue']
    )
    
    p2 = Planet(
        'Mars',
        x=p1.x + EARTH_MARS_DISTANCE/50,
        y=p1.y + EARTH_MARS_DISTANCE/50,
        vx=-INITIAL_VELOCITY,
        vy=0,
        m=MARS_MASS,
        color=COLORS['red']
    )

    p3 = Planet(
        'X Planet',
        x=p1.x + EARTH_MARS_DISTANCE/50,
        y=p1.y - EARTH_MARS_DISTANCE/200,
        vx=0,
        vy=INITIAL_VELOCITY,
        m=X_MASS,
        color=COLORS['green']
    )

    # Initial state vector for simulation
    y0 = []
    y0.extend(p1.get_state())
    y0.extend(p2.get_state())
    y0.extend(p3.get_state())

    for i in range(len(t) - 1):

        event = pygame.event.poll()

        # Window close button
        if event.type == pygame.QUIT:
            break
        elif event.type == pygame.MOUSEBUTTONDOWN:
            paused()

        #######################################################################
        # SIMULATION
        #######################################################################

        t0, tf = t[i], t[i+1]

        args = (p1, p2, p3)
        sol = solve_ivp(model, (t0, tf), y0, args=args)
        y0 = sol.y[:, -1]
        
        p1.set_state(y0[:4])
        p2.set_state(y0[4:8])
        p3.set_state(y0[8:])

        #######################################################################
        # DRAW
        #######################################################################

        # Re-paint the whole surface
        main_surface.fill(COLORS['black'])

        # Paint each planet on the screen
        p1.draw(main_surface)
        p2.draw(main_surface)
        p3.draw(main_surface)

        # Clean and write text on a corner
        pygame.draw.rect(main_surface,COLORS['black'], (100,100,220,40))
        myfont = pygame.font.SysFont("Comic Sans MS", 30)
        label = myfont.render(f"Day {i}", 1, COLORS['red'])
        main_surface.blit(label, (100, 100))

        # Display the surface
        pygame.display.flip() 

    pygame.quit()

main()