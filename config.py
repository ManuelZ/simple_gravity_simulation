# Screen size
SURFACE_SIZE_WIDTH = 1000 # 1920
SURFACE_SIZE_HEIGHT = 1000 # 1080

# Universal gravitational constant
G = 6.6743e-11

SUN_MASS = 1.9e30

# In Pygame units
SUN_SIZE = 20

# Distance between Earth and Mars 
EARTH_MARS_DISTANCE = 54.6e6 # km

# Ratio to draw result to scale
# KM_PER_PX = EARTH_MARS_DISTANCE / (600/0.05) # km/px
KM_PER_PX = EARTH_MARS_DISTANCE / (SURFACE_SIZE_WIDTH/0.05) # 4265.625 km/px 
KM_PER_PX = 100000  # km/px

# A base initial velocity to give to each planet
INITIAL_VELOCITY = 2 # km/s

N_PLANETS = 9

COLORS = {
    'light_blue' : (0, 200, 255),
    'red'  : (255, 0, 0),
    'blue'  : (0, 0, 255),
    'white' : (255, 255, 255),
    #'black' : (0, 0, 0),
    'green' : (0, 255, 0)
}

print(f'Using a ratio of {KM_PER_PX} km/px')


