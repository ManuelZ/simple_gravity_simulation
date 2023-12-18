# Built-in imports
from math import radians
from math import cos
from math import sin
import random

# External imports
import pygame
import numpy as np
from scipy.integrate import solve_ivp

# Local imports
from planet import Planet
from utils import px2km
from utils import paused
from utils import constrain_planet_to_screen
from config import (
    SURFACE_SIZE_WIDTH,
    SURFACE_SIZE_HEIGHT,
    INITIAL_VELOCITY,
    COLORS,
    N_PLANETS,
    SUN_MASS,
    SUN_SIZE
)


random.seed(42)

MIN = 999999
MAX = -float("inf")
# Total number of seconds to simulate
t_sim = 50 * 365 * 24 * 3600 # seconds

# Time chunks to give to the solver
resolution = 3600*24  # 1 day == 3600*24 seconds

t = np.linspace(0, t_sim, int((t_sim / resolution) + 1))


def model(t, X, *planets):
    """
    Refer to https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_ivp.html
    """

    Xdot = []
    for i,planet in enumerate(planets):

        # Extract planet state from state vector
        x, xdot, y, ydot = X[i*4 : (i*4)+4]

        # Calculate forces on the planet due to the other planets
        other_planets = [p for p in planets if planet != p]
        Fx_on_p, Fy_on_p = planet.forces(other_planets)
        planet_acc_x = planet.get_acc(Fx_on_p)
        planet_acc_y = planet.get_acc(Fy_on_p)

        Xdot.extend([
            xdot,
            planet_acc_x,
            ydot,
            planet_acc_y
        ])

    return Xdot


def main():
    """ Set up the game and run the main game loop """
    
    ###########################################################################
    # PYGAME SETUP
    ###########################################################################

    pygame.init()
    pygame.font.init()
    pygame.display.set_caption('Gravity simulation')

    # Create surface of (width, height)
    main_surface = pygame.display.set_mode((SURFACE_SIZE_WIDTH, SURFACE_SIZE_HEIGHT))


    ###########################################################################
    # DEFINE PLANETS
    ###########################################################################
 
    sun = Planet(
        f'SUN',
        x=px2km(SURFACE_SIZE_WIDTH)/2,
        y=px2km(SURFACE_SIZE_WIDTH)/2,
        vx=0,
        vy=0,
        m=SUN_MASS,
        color=COLORS["red"],
        size=SUN_SIZE
    )

    planets = [sun]

    thetas = np.linspace(0, 360, N_PLANETS+1)
    center_x = px2km(SURFACE_SIZE_WIDTH)/2
    center_y = px2km(SURFACE_SIZE_WIDTH)/2
    
    for i in range(N_PLANETS):
        theta = radians(thetas[i])

        # Random distance from center 
        lower_limit = int(px2km(SURFACE_SIZE_WIDTH)/6)
        upper_limit = int(px2km(SURFACE_SIZE_WIDTH)/4)
        r = random.randint(lower_limit, upper_limit)

        # The unit tangent vector is the derivative of the position vector 
        # with respect to theta, normalized.
        # r(theta) = { r*cos(theta), r*sin(theta) }
        # d_r/d_theta = { -r * sin(theta), r* cos(theta) }
        d = np.linalg.norm([r*cos(theta), r*sin(theta)])
        vx = INITIAL_VELOCITY * (-r * sin(theta)) / d
        vy = INITIAL_VELOCITY * (r * cos(theta)) / d
        
        mass= random.randint(6.39e23, 6e24)
        
        # Calculate the size of the planets, based on their mass,
        # but scaled because the sun is huge
        planet_size = mass * (SUN_SIZE/SUN_MASS) * 1.1e5
        planet_color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))

        planets.append(
            Planet(
                f'Planet{i}',
                x = center_x + r * cos(theta),
                y = center_y + r * sin(theta),
                vx=vx,
                vy=vy,
                m=mass,
                color=planet_color,
                size=planet_size
            )
        )

    # Initial state vector for simulation
    initial_state = []
    for p in planets:
        initial_state.extend(p.get_state())

    for i in range(len(t) - 1):

        event = pygame.event.poll()

        # Window close button
        if event.type == pygame.QUIT:
            break
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            paused()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                break


        #######################################################################
        # SIMULATION
        #######################################################################

        t0, tf = t[i], t[i+1]

        # To manually update velocities in each iteration
        # set y0, not Planet.set_state
        sol = solve_ivp(model, (t0, tf), y0=initial_state, args=planets, method="LSODA")
        
        # The initial state of the next iteration will be the last step of the current result
        initial_state = sol.y[:, -1]
        
        new_initial_state = []
        for j in range(len(planets)):
            x, xdot, y, ydot = initial_state[j*4 : (j*4)+4]
            x, xdot, y, ydot = constrain_planet_to_screen(x, xdot, y, ydot)
            new_initial_state.extend([x, xdot, y, ydot])
            planets[j].set_state([x, xdot, y, ydot])

        initial_state = new_initial_state


        #######################################################################
        # DRAW
        #######################################################################

        # Re-paint the whole surface
        main_surface.fill((0, 0, 0)) # black

        for p in planets:
            p.draw(main_surface)

        # Clean and write text on a corner
        #pygame.draw.rect(main_surface, (0,0,0), (100,100,220,40))
        myfont = pygame.font.SysFont("Comic Sans MS", 30)
        label = myfont.render(f"Day {i}", 1, COLORS['red'])
        main_surface.blit(label, (100, 500))  # x, y

        # Display the surface
        pygame.display.flip()
        # pygame.time.wait(50)

    pygame.quit()


if __name__ == "__main__":
    main()