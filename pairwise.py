import fields
import logrange
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr
import numerical
import numpy as np


async def plot_pairwise(param_list, param1, param2):

    omega_s_array, pair_array = numerical.calc_pair_array(param_list)

    param_labels = ["$V_D$", "$d_0$", "$V_T$", "$T_D$", "$D_R$", r"$\Delta$"]

    log_data = np.log10(omega_s_array)
    global_vmin = np.nanmin(log_data)
    global_vmax = np.nanmax(log_data)
    levels = np.linspace(global_vmin, global_vmax, 100)
    values = logrange.get_small()

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

    ax: plt.Axes
    fig, ax = plt.subplots()
    CS = ax.contourf(values, values, log_data[index], levels=levels)
    for a in CS.collections:
        a.set_edgecolor("face")
    ax.yaxis.set_major_formatter(tkr.FormatStrFormatter("%.1e"))
    ax.xaxis.set_major_formatter(tkr.FormatStrFormatter("%.1e"))
    ax.set_ylabel(f"Fold change in {param_labels[param1_n]}")
    ax.set_xlabel(f"Fold change in {param_labels[param2_n]}")
    ax.set_yscale("log")
    ax.set_xscale("log")
    ax.set_ylim(1e-2, 1e2)
    ax.set_xlim(1e-2, 1e2)
    ax.axhline(1, c="k", ls="--", alpha=0.5)
    ax.axvline(1, c="k", ls="--", alpha=0.5)
    fig.colorbar(
        CS,
        label=r"log$_{10}$(fold change in $\omega_s$)",
        ax=ax,
        fraction=0.046,
        pad=0.04,
        format=tkr.FormatStrFormatter("%.1f"),
    )
    fig.tight_layout()
