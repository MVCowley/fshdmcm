import fields
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from numerical import (
    calc_omega_s,
    calc_pair_array,
    calc_singlet_omega_s_array,
)
import numpy as np


def singlet_to_diff(
    singlet_omega_s_array, pair_array, omega_s_array, param_list
):
    values = np.logspace(-2, 2, 100)
    # Create object to populate with calculated absorption times
    diff_omega_s_array = np.full(
        (len(pair_array), len(values), len(values)), np.nan
    )

    diff_combination = 0
    for i in range(len(param_list) - 1):
        for j in range(i + 1, len(param_list)):
            i_values = values
            for index0, i_value in enumerate(i_values):
                j_values = values
                for index1, j_value in enumerate(j_values):
                    diff_omega_s_array[
                        diff_combination, index0, index1
                    ] = omega_s_array[diff_combination, index0, index1] - (
                        singlet_omega_s_array[i, index0]
                        + singlet_omega_s_array[j, index1]
                    )
            diff_combination += 1
    return diff_omega_s_array


def interaction_plot(params, param1, param2):

    omega_s_array, pair_array = calc_pair_array(params)
    singlets = calc_singlet_omega_s_array(params)
    diff = singlet_to_diff(singlets, pair_array, omega_s_array, params)

    param_labels = ["$V_D$", "$d_0$", "$V_T$", "$T_D$", "$D_r$", r"$\Delta$"]

    # Calculate consistent vmin and vmax for color scale across all plots
    values = np.logspace(-2, 2, 100)
    base = calc_omega_s(params)
    log_data = diff / base + 1
    cparam = 45
    levels = np.linspace(-cparam, cparam, int((cparam - (-cparam)) / 0.1) + 1)

    # Create pairwise heatmap plot
    param_converter = {
        field: n for n, field in enumerate(fields.get_field_strings())
    }

    param1_n = param_converter[param1]
    param2_n = param_converter[param2]

    if param1_n == param2_n:
        raise ValueError(
            "Can't compute the interaction of a parameter with itself"
        )

    # find i, j in pair_array
    for n, i in enumerate(pair_array):
        if i[0] == param1_n and i[1] == param2_n:
            index = n

    ax: plt.Axes
    fig, ax = plt.subplots(figsize=(4, 4))
    CS = ax.contourf(
        values,
        values,
        log_data[index],
        levels=levels,
        cmap="RdBu",
    )
    for a in CS.collections:
        a.set_edgecolor("face")
    ax.set_xlim(1e-2, 1e0)
    ax.set_ylim(1e-2, 1e2)
    ax.yaxis.set_major_formatter(FormatStrFormatter("%.1e"))
    ax.xaxis.set_major_formatter(FormatStrFormatter("%.1e"))
    ax.set_ylabel(f"Fold change in {param_labels[param1_n]}")
    ax.set_xlabel(f"Fold change in {param_labels[param2_n]}")
    ax.set_yscale("log")
    ax.set_xscale("log")
    ax.axhline(1, c="k", ls="--", alpha=0.5)
    ax.axvline(1, c="k", ls="--", alpha=0.5)
    ax.set_box_aspect(1)
    fig.colorbar(CS, label=r"$\mathbf{I}_{ij}$")
    fig.tight_layout()
