import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation
from matplotlib.patches import Circle
from mpl_toolkits.mplot3d.axes3d import Axes3D
from numpy import cos, sin

from scipy.constants import kilo, pi
import cv2

from scipy.integrate import solve_ivp
from matplotlib.animation import FuncAnimation
mpl.use('TkAgg')
import constants as const

'''
cv2.namedWindow("Orbit",cv2.WINDOW_AUTOSIZE)

im_old = np.zeros((500,500))

for i in range(360*4):
    xc = 250
    yc = 250
    im = im_old.copy()
    x = int(125*np.cos((i**2)*np.pi/180.0)+xc)
    y = int(125*np.sin(i*np.pi/180.0)+yc)
    im[(x-2):(x+3),(y-2):(y+3)] = 255
    im_old[x,y] = 128
    cv2.imshow("Orbit",im)
    cv2.waitKey(10);
'''

def orbit_equations(t, y, mu):
    r = y[:3]
    v = y[3:]
    r_norm = np.linalg.norm(r)
    drdt = v
    dvdt = -mu * r / r_norm ** 3
    return np.concatenate([drdt, dvdt])


# Parameters
mu = 398600.4418  # Earth's gravitational parameter (km^3/s^2)
y0 = np.array([6500, 0, 0, 0, 7.5, 0])  # Initial conditions (x,y,z,vx,vy,vz)
t_span = (0, 100000)  # Simulation time (s)
t_eval = np.linspace(t_span[0], t_span[1], int(t_span[1]/20))  # Time points

# Solve the ODE
sol = solve_ivp(orbit_equations, t_span, y0, args=(mu,), t_eval=t_eval, method='RK45')

# Extract position data - ensure we get arrays
x = np.array(sol.y[0])
y = np.array(sol.y[1])

# Set up figure
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(min(-7000,1.2 * min(x)), max(7000,1.2 * max(x)))
ax.set_ylim(min(-7000,1.2 * min(y)), max(7000,1.2 * max(y)))
ax.set_aspect('equal')
ax.grid()

# Add Earth
earth = plt.Circle((0, 0), 6371, color='blue', alpha=0.3)
ax.add_patch(earth)

# Initialize plot elements
trail, = ax.plot([], [], 'b-', lw=1, alpha=0.5)  # Orbit path
point, = ax.plot([], [], 'ro', ms=6)  # Satellite


# Initialize with empty sequences
def init():
    trail.set_data([], [])
    point.set_data([], [])
    return trail, point


# Update function - ensure we're passing sequences
def update(frame):
    # Get all points up to current frame
    x_data = x[:frame + 1]  # +1 to include current frame
    y_data = y[:frame + 1]

    # Current position (as length-1 arrays)
    x_point = np.array([x[frame]])
    y_point = np.array([y[frame]])

    trail.set_data(x_data, y_data)
    point.set_data(x_point, y_point)
    return trail, point


# Create animation
ani = FuncAnimation(
    fig,
    update,
    frames=len(x),  # Number of frames matches data points
    init_func=init,
    blit=True,
    interval=20,
    repeat=True
)

# To display in different environments:
plt.show()