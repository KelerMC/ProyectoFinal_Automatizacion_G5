import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint


class CartPoleSystem:
    def __init__(self, pendulum_pid, cart_pid):
        # System parameters
        self.M = 1.0  # Mass of cart (kg)
        self.m = 0.1  # Mass of pendulum (kg)
        self.l = 0.5  # Length of pendulum (m)
        self.g = 9.81  # Gravity (m/s^2)

        # Controller parameters for pendulum (provided by user)
        self.pendulum_pid = pendulum_pid

        # Controller parameters for cart (provided by user)
        self.cart_pid = cart_pid

        # Reference positions
        self.x_ref = 0.0  # Desired cart position
        self.theta_ref = 0.0  # Desired pendulum angle

    def system_dynamics(self, state, t):
        x, theta, x_dot, theta_dot = state

        # Calculate errors
        theta_error = theta - self.theta_ref
        x_error = x - self.x_ref

        # Update integral errors
        dt = 0.01  # Small time step for integral calculation
        self.pendulum_pid['integral_error'] += theta_error * dt
        self.cart_pid['integral_error'] += x_error * dt

        # Calculate PID control signals
        pendulum_control = (self.pendulum_pid['kp'] * theta_error +
                            self.pendulum_pid['ki'] * self.pendulum_pid['integral_error'] +
                            self.pendulum_pid['kd'] * theta_dot)

        cart_control = (self.cart_pid['kp'] * x_error +
                        self.cart_pid['ki'] * self.cart_pid['integral_error'] +
                        self.cart_pid['kd'] * x_dot)

        # Combined control force
        F = cart_control + pendulum_control

        # System matrices
        M = np.array([[self.M + self.m, self.m * self.l * np.cos(theta)],
                      [self.m * self.l * np.cos(theta), self.m * self.l ** 2]])

        C = np.array([[-self.m * self.l * theta_dot ** 2 * np.sin(theta) + F],
                      [self.m * self.g * self.l * np.sin(theta)]])

        # Solve for accelerations
        acc = np.linalg.solve(M, C)
        x_ddot = acc[0][0]
        theta_ddot = acc[1][0]

        return [x_dot, theta_dot, x_ddot, theta_ddot]

    def simulate(self, t_span, initial_state):
        t = np.linspace(0, t_span, int(t_span / 0.01))
        solution = odeint(self.system_dynamics, initial_state, t)
        return t, solution

    def plot_results(self, t, solution):
        plt.figure(figsize=(12, 10))
        
        # Cart position
        plt.subplot(3, 1, 1)
        plt.plot(t, solution[:, 0], 'b-', label='Cart Position')
        plt.plot(t, np.ones_like(t) * self.x_ref, 'r--', label='Reference')
        plt.grid(True)
        plt.legend()
        plt.ylabel('Position (m)')
        plt.title('Cart-Pole System Response')
        
        # Pendulum angle
        plt.subplot(3, 1, 2)
        plt.plot(t, np.degrees(solution[:, 1]), 'g-', label='Pendulum Angle')
        plt.plot(t, np.degrees(np.ones_like(t) * self.theta_ref), 'r--', label='Reference')
        plt.grid(True)
        plt.legend()
        plt.ylabel('Angle (degrees)')
        
        # Control signals
        plt.subplot(3, 1, 3)
        cart_control = (self.cart_pid['kp'] * (solution[:, 0] - self.x_ref) + 
                       self.cart_pid['kd'] * solution[:, 2])
        pendulum_control = (self.pendulum_pid['kp'] * solution[:, 1] + 
                          self.pendulum_pid['kd'] * solution[:, 3])
        plt.plot(t, cart_control, 'b-', label='Cart Control')
        plt.plot(t, pendulum_control, 'g-', label='Pendulum Control')
        plt.grid(True)
        plt.legend()
        plt.xlabel('Time (s)')
        plt.ylabel('Force (N)')
        
        plt.tight_layout()
        plt.show()

def plot_pendulum_cart_response(pendulum_pid, cart_pid, t_span=40.0, initial_state=[0.0, np.radians(30.0), 0.0, 0.0]):
    # Create system with given PID values
    system = CartPoleSystem(pendulum_pid, cart_pid)
    
    # Run simulation
    t, solution = system.simulate(t_span, initial_state)
    
    # Plot results
    system.plot_results(t, solution)


def main():
    #Prueba normal
    # Set PID parameters for pendulum and cart
    cart_pid = {'kp': 1, 'ki': 0, 'kd': 1, 'integral_error': 0}
    t_span = 20.0  # seconds
    initial_state = [0.0, np.radians(30.0), 0.0, 0.0]  # [x, theta, x_dot, theta_dot]
    
    """"
    pendulum_pid = {'kp': 40, 'ki': 0, 'kd': 4, 'integral_error': 0}
    
    # Simulation parameters
    
    
    # Run simulation and plot results
    plot_pendulum_cart_response(pendulum_pid, cart_pid, t_span, initial_state)
"""
    #Pruebas de variantes de controlador
    #P(ki, kd = 0)
    #plot_pendulum_cart_response({'kp': 10, 'ki': 0, 'kd': 0, 'integral_error': 0}, cart_pid, t_span, initial_state)
    #plot_pendulum_cart_response({'kp': 50, 'ki': 0, 'kd': 0, 'integral_error': 0}, cart_pid, t_span, initial_state)
    #plot_pendulum_cart_response({'kp': 100, 'ki': 0, 'kd': 0, 'integral_error': 0}, cart_pid, t_span, initial_state)

    #PI(kd = 0)
    #plot_pendulum_cart_response({'kp': 50, 'ki': 0.1, 'kd': 0, 'integral_error': 0}, cart_pid, t_span, initial_state)
    #plot_pendulum_cart_response({'kp': 50, 'ki': 1, 'kd': 0, 'integral_error': 0}, cart_pid, t_span, initial_state)
    #plot_pendulum_cart_response({'kp': 50, 'ki': 10, 'kd': 0, 'integral_error': 0}, cart_pid, t_span, initial_state)
    
    #PD (ki = 0)
    plot_pendulum_cart_response({'kp': 100, 'ki': 0, 'kd': 1, 'integral_error': 0}, cart_pid, t_span, initial_state)
    plot_pendulum_cart_response({'kp': 400, 'ki': 0, 'kd': 10, 'integral_error': 0}, cart_pid, t_span, initial_state)
    plot_pendulum_cart_response({'kp': 500, 'ki': 0, 'kd': 50, 'integral_error': 0}, cart_pid, t_span, initial_state)

    #Pruebas carro
    pendulum_pid = {'kp': 200, 'ki': 0, 'kd': 50, 'integral_error': 0}
    plot_pendulum_cart_response(pendulum_pid, {'kp': 50, 'ki': 0, 'kd': 100, 'integral_error': 0}, t_span, initial_state)
    plot_pendulum_cart_response(pendulum_pid, {'kp': 100, 'ki': 0, 'kd': 50, 'integral_error': 0}, t_span, initial_state)
    plot_pendulum_cart_response(pendulum_pid, {'kp': 10, 'ki': 0, 'kd': 10, 'integral_error': 0},  t_span, initial_state)
if __name__ == "__main__":
    main()
