import unittest
import sys
import os

from pso import pso_simple
from pso.cost_functions import sphere


class TestPSO(unittest.TestCase):

    def test_evaluate(self):
        """
        This test checks whether the evaluate method correctly evaluates the particle's position using the given cost function.
        """
        # Create a particle
        particle = pso_simple.Particle([1, 2])

        # Define a cost function
        def cost_func(position):
            return sum(position)

        # Evaluate the particle's position using the cost function
        particle.evaluate(cost_func)

        # Check if the particle's best position and error are updated correctly
        self.assertEqual(particle.pos_best_i, [1, 2])
        self.assertEqual(particle.err_best_i, 3)

    def test_minimize(self):
        """
        This test checks whether the minimize function correctly minimizes the given cost function.
        """
        x0 = [5, 5]
        bounds = [(-10, 10), (-10, 10)]
        opt = pso_simple.minimize(sphere, x0, bounds, num_particles=15, maxiter=30, verbose=False)

        # Check if the optimized solution is better than the initial solution
        self.assertLess(sphere(opt[1]), sphere(x0))

    def test_update_velocity(self):
        """
        This test checks whether the update_velocity method correctly updates the particle's velocity."""
        # Create a particle
        particle = pso_simple.Particle([1, 2])

        # Set the particle's best position
        particle.pos_best_i = [3, 4]

        # Set the particle's current position
        particle.position_i = [2, 3]

        # Set the particle's velocity
        particle.velocity_i = [0.5, 0.5]

        # Set the global best position
        pos_best_g = [5, 6]

        # Update the particle's velocity
        particle.update_velocity(pos_best_g)

        # Check if the particle's velocity is updated correctly
        self.assertNotEqual(particle.velocity_i, [0.5, 0.5])

    def test_update_position(self):
        """
        This test checks whether the update_position method correctly updates the particle's position."""
        # Create a particle
        particle = pso_simple.Particle([1, 2])

        # Set the particle's current position
        particle.position_i = [2, 3]

        # Set the particle's velocity
        particle.velocity_i = [0.5, 0.5]

        # Set the bounds of the search space
        bounds = [(-10, 10), (-10, 10)]

        # Update the particle's position
        particle.update_position(bounds)

        # Check if the particle's position is updated correctly
        self.assertEqual(particle.position_i, [2.5, 3.5])
        self.assertGreaterEqual(particle.position_i[0], bounds[0][0])
        self.assertLessEqual(particle.position_i[0], bounds[0][1])
        self.assertGreaterEqual(particle.position_i[1], bounds[1][0])
        self.assertLessEqual(particle.position_i[1], bounds[1][1])


if __name__ == '__main__':
    unittest.main()