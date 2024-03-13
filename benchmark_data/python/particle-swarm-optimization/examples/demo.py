from pso import pso_simple
from pso.cost_functions import sphere

initial=[5,5]
bounds=[(-10,10),(-10,10)]
pso_simple.minimize(sphere, initial, bounds, num_particles=15, maxiter=30, verbose=True)