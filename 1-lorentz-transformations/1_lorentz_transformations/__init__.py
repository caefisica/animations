import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import FancyArrow

def lorentz_transform(x, t, v):
    c = 1  # speed of light
    gamma = 1 / np.sqrt(1 - v**2/c**2)
    x_prime = gamma * (x - v*t)
    t_prime = gamma * (t - v*x/c**2)
    return x_prime, t_prime

fig, ax = plt.subplots()
x = np.linspace(-2, 2, 10)
lines = [np.full_like(x, i) for i in np.linspace(0, 2, 10)]

# Lines + two light cones
line_objs = [ax.plot([], [], 'o:', ms=3, lw=1, alpha=0.5, color='grey')[0] for _ in range(len(lines)+2)]

object_speeds = [0.5, 0.75, 1.0]
colors = ['red', 'blue', 'green']  # colors for the arrows

def init():
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_xlabel('x')
    ax.set_ylabel('t')
    return line_objs

def update(v):
    for patch in reversed(ax.patches):  # remove all patches
        patch.remove()
    for line, line_obj in zip(lines, line_objs[:-2]):
        x_prime, t_prime = lorentz_transform(x, line, v)
        line_obj.set_data(x_prime, t_prime)
    for speed, color in zip(object_speeds, colors):
        x_prime, t_prime = lorentz_transform(x[-1], speed, v)
        arrow = FancyArrow(0, 0, x_prime, t_prime, width=0.02, color=color, alpha=0.5)
        ax.add_patch(arrow)  # add a new arrow
    line_objs[-2].set_data(x, x)  # Light cone
    line_objs[-1].set_data(x, -x)  # Light cone
    return line_objs

ani = FuncAnimation(fig, update, frames=np.linspace(0, 0.9, 100), 
                    init_func=init, blit=True)

# Save the animation
ani.save('lorentz_transform_light_cone_arrow.mp4', writer='ffmpeg')
