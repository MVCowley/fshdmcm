from numerical import calc_omega_s, calc_singlet_omega_s_array
import numpy as np
import matplotlib.pyplot as plt


def find_max_deriv(param_n, omega_s_array, values):
    param_data = omega_s_array[param_n]
    grad = np.gradient(param_data, values)
    return np.amax(np.absolute(grad))


def find_endog_deriv(param_n, omega_s_array, values):
    param_data = omega_s_array[param_n]
    grad = np.gradient(param_data, values)
    endog = (np.abs(param_data - 1)).argmin()
    return np.absolute(grad[endog])


def plot_sensitivity(param_list):

    values = np.logspace(-4, 4, 100)
    base = calc_omega_s(param_list)

    omega_s_array = calc_singlet_omega_s_array(param_list) / base

    max_derivs = [
        find_max_deriv(i, omega_s_array, values)
        for i, _ in enumerate(omega_s_array)
    ]

    endog_derivs = [
        find_endog_deriv(i, omega_s_array, values)
        for i, _ in enumerate(omega_s_array)
    ]

    ax: plt.Axes
    fig, ax = plt.subplots(figsize=(4, 4))

    rate_labels = ["$V_D$", "$d_0$", "$V_T$", "$T_D$", "$D_r$", r"$\Delta$"]
    colors = ["C0", "C1", "C2", "C3", "C4", "C5"]
    x = np.arange(len(rate_labels))  # the x coordinates of the bars
    width = 0.4  # the width of the bars

    # Plot endog_derivs
    ax.bar(x, endog_derivs, width, color=colors, label="Endogenous derivatives")

    # Plot max_derivs
    ax.bar(
        x + width,
        max_derivs,
        width,
        color=colors,
        label="Maximum derivatives",
        alpha=0.5,
    )

    ax.legend()

    ax.set_xticks(x + width / 2)
    ax.set_xticklabels(rate_labels)

    ax.set_yscale("log")
    ax.set_ylabel(r"$\omega'$")

    fig.tight_layout()
