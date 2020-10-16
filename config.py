# Screen size
SURFACE_SIZE = 600   

# Universal gravitational constant
G = 6.6743e-11

# PLANETS' MASS
EARTH_MASS = 5.97e24  # kg
MARS_MASS = 6.39e23   # kg
X_MASS = 6e24         # kg

# Distance between Earth and Mars 
EARTH_MARS_DISTANCE = 54.6e6 # km

# Ratio to draw result to scale
KM_PER_PX = EARTH_MARS_DISTANCE / (SURFACE_SIZE/0.05) # km/px

# A base initial velocity to give to each planet
INITIAL_VELOCITY = 0.01 # km/s

COLORS = {
    'light_blue' : (0, 200, 255),
    'red'  : (255, 0, 0),
    'blue'  : (0, 0, 255),
    'white' : (255, 255, 255),
    'black' : (0, 0, 0),
    'green' : (0, 255, 0)
}

print(f'Using a ratio of {KM_PER_PX} km/px')


