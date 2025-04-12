import numpy as np
import matplotlib.pyplot as plt
from ipysim.simulations.simulate_maglev import simulate as base_simulate, plot_maglev
from ipywidgets import interact, FloatSlider, Checkbox

def simulate_with_noise(params, state0, T, dt, Kp, Kd):
    from ipysim.simulations.simulate_maglev import maglev_measurements as base_meas
    def noisy_measurements(state, m, mu0):
        y, y_dot = base_meas(state, m, mu0)
        y += np.random.normal(0, 0.001)
        y_dot += np.random.normal(0, 0.001)
        return y, y_dot

    from ipysim.simulations import simulate_maglev
    original_meas = simulate_maglev.maglev_measurements
    simulate_maglev.maglev_measurements = noisy_measurements
    try:
        return base_simulate(params, state0, T, dt, Kp, Kd)
    finally:
        simulate_maglev.maglev_measurements = original_meas

def maglev_with_noise_simulation(params, state0=None, T=5.0, dt=0.001, **slider_values):
    Kp = slider_values.get("Kp", 300.0)
    Kd = slider_values.get("Kd", 10.0)
    init_x = slider_values.get("init_x", 0.0)
    init_z = slider_values.get("init_z", 0.0443)
    noise = slider_values.get("noise", False)

    state0 = [init_x, init_z, 0.0, 0.0, 0.0, 0.0]

    if noise:
        return simulate_with_noise(params, state0, T, dt, Kp, Kd)
    else:
        return base_simulate(params, state0, T, dt, Kp, Kd)

def plot_maglev_with_noise(t, sol):
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.plot(t, sol[:, 1], label='z')
    plt.plot(t, sol[:, 0], label='x')
    plt.xlabel('Time [s]')
    plt.ylabel('Position [m]')
    plt.title('Position of Levitating Magnet (x, z)')
    plt.grid(True)
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(sol[:, 0], sol[:, 1], label='Trajectory')
    plt.plot(sol[0, 0], sol[0, 1], 'go', markersize=8, label='Initial')
    plt.plot(sol[-1, 0], sol[-1, 1], 'ro', markersize=8, label='Final')
    plt.xlabel('x')
    plt.ylabel('z')
    plt.title('Phase Plot of x vs z')
    plt.grid(True)
    plt.xlim(-0.01, 0.01)
    plt.ylim(0, 0.1)
    plt.legend()
    plt.tight_layout()
    plt.show(block=False) # To avoid redundant plots

def run_simulation(init_x, init_z, noise):
    params = {
        "M": 0.075,
        "m": 9.375,
        "l": 0.046,
        "g": 9.81,
        "m_support": 0.6250,
        "k": 0.0377,
        "J": 0.12e-4,
        "mu0": 4 * np.pi * 1e-7
    }

    Kp, Kd = 300.0, 10.0
    T = 5
    dt = 0.001

    state0 = [init_x, init_z, 0.0, 0.0, 0.0, 0.0]
    t, sol = maglev_with_noise_simulation(params, state0=state0, T=T, dt=dt, Kp=Kp, Kd=Kd, noise=noise)
    plot_maglev_with_noise(t, sol)