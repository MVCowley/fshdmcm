import fields
import logrange
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import numerical
import numpy as np


def singlet_to_diff(
    singlet_omega_s_array, pair_array, omega_s_array, param_list
):
    values = logrange.get_small()
    diff_omega_s_array = np.full(
        (len(pair_array), len(values), len(values)), np.nan
    )

    diff_combination = 0
    for i in range(len(param_list) - 1):
        for j in range(i + 1, len(param_list)):
            i_values = values
            for index0, _ in enumerate(i_values):
                j_values = values
                for index1, _ in enumerate(j_values):
                    diff_omega_s_array[
                        diff_combination, index0, index1
                    ] = omega_s_array[diff_combination, index0, index1] - (
                        singlet_omega_s_array[i, index0]
                        + singlet_omega_s_array[j, index1]
                    )
            diff_combination += 1
    return diff_omega_s_array


async def interaction_plot(params, param1, param2):

    omega_s_array, pair_array = numerical.calc_pair_array(params)
    singlets = numerical.calc_singlet_omega_s_array(params)
    diff = singlet_to_diff(singlets, pair_array, omega_s_array, params)

    param_labels = ["$V_D$", "$d_0$", "$V_T$", "$T_D$", "$D_r$", r"$\Delta$"]

    values = logrange.get_small()
    base = numerical.calc_omega_s(params)
    norm_data = diff / base + 1
    cparam = np.max(norm_data)
    levels = np.linspace(-cparam, cparam, int((cparam - (-cparam)) / 0.1) + 1)

    param_converter = {
        field: n for n, field in enumerate(fields.get_field_strings())
    }

    param1_n = param_converter[param1]
    param2_n = param_converter[param2]

    if param1_n == param2_n:
        raise ValueError(
            "Can't compute the interaction of a parameter with itself"
        )
    if param1_n > param2_n:
        param1_n, param2_n = param2_n, param1_n

    for n, i in enumerate(pair_array):
        if i[0] == param1_n and i[1] == param2_n:
            index = n

    axs: list[plt.Axes]
    fig, axs = plt.subplots(ncols=2, figsize=(7, 14))
    ax = axs[0]
    CS = ax.contourf(
        values,
        values,
        norm_data[index],
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
    fig.colorbar(
        CS, label=r"$\mathbf{I}_{ij}$", ax=ax, fraction=0.046, pad=0.04
    )
    fig.tight_layout()

    ax = axs[1]
    combined_array = np.empty((6, 6))

    np.fill_diagonal(combined_array, np.nan)

    for combo, pair in zip(norm_data, pair_array):
        combined_array[pair[0], pair[1]] = np.nanmax(combo)
        combined_array[pair[1], pair[0]] = np.nanmin(combo)

    if np.nanmin(combined_array) < np.nanmax(combined_array):
        lim_func = np.nanmax
    elif np.nanmax(combined_array) < np.nanmin(combined_array):
        lim_func = lambda x: -1 * np.nanmin(x)

    limits = lim_func(combined_array)

    cax = ax.imshow(
        combined_array,
        interpolation="nearest",
        cmap="RdBu",
        vmin=-limits,
        vmax=limits,
    )
    ax.set_xticks(np.arange(len(param_labels)))
    ax.set_yticks(np.arange(len(param_labels)))
    ax.set_xticklabels(param_labels)
    ax.set_yticklabels(param_labels)

    fig.colorbar(
        cax, label=r"$\mathbf{I}_{ij}$", ax=ax, fraction=0.046, pad=0.04
    )
    fig.tight_layout()
