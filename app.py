import numpy as np
from shiny.express import input, render, ui
import single_markov_chain
import matplotlib.pyplot as plt

ui.page_opts(fillable=True)

with ui.sidebar():
    ui.input_selectize(
        "param",
        "Select $x$-axis parameter",
        [
            "DUX4 transcription rate",
            "DUX4 mRNA degredation rate",
            "D4T transcription rate",
            "DUX4 mRNA translation rate",
            "D4T$^{+}$ myonuclear apoptosis rate",
            "DUX4 & D4T syncytial diffusion rate",
        ],
    )
    "Fixed parameters"
    ui.input_slider(
        "vd",
        "log10(Fold change in DUX4 transcription rate)",
        np.log10(1e-4),
        np.log10(1e4),
        np.log10(1),
    )
    ui.input_slider(
        "d0",
        "log10(Fold change in DUX4 mRNA degredation rate)",
        np.log10(1e-4),
        np.log10(1e4),
        np.log10(1),
    )
    ui.input_slider(
        "vt",
        "log10(Fold change in DUX4 target transcription rate)",
        np.log10(1e-4),
        np.log10(1e4),
        np.log10(1),
    )
    ui.input_slider(
        "td",
        "log10(Fold change in DUX4 translation rate)",
        np.log10(1e-4),
        np.log10(1e4),
        np.log10(1),
    )
    ui.input_slider(
        "dr",
        "log10(Fold change in death rate)",
        np.log10(1e-4),
        np.log10(1e4),
        np.log10(1),
    )
    ui.input_slider(
        "delta",
        "log10(Fold change in DUX4 syncytial diffusion rate)",
        np.log10(1e-4),
        np.log10(1e4),
        np.log10(1),
    )

"Single parameter plot"

with ui.card(full_screen=True):

    @render.plot
    def mc_plot():
        real_params = [
            (0.00211) * 10 ** input.vd(),
            (0.246) * 10 ** input.d0(),
            (6.41) * 10 ** input.vt(),
            (1 / 13) * 10 ** input.td(),
            (1 / 20.2) * 10 ** input.dr(),
            (0.04023596) * 10 ** input.delta(),
        ]

        values, omega_s = single_markov_chain.calc_array(
            input.param(), real_params, -4, 4
        )

        colours = {
            "DUX4 transcription rate": "C0",
            "DUX4 mRNA degredation rate": "C1",
            "DUX4 target transcription rate": "C2",
            "DUX4 translation rate": "C3",
            "Death rate": "C4",
            "DUX4 syncytial diffusion rate": "C5",
        }

        fig, ax = plt.subplots(figsize=(3, 3))
        ax.plot(values, omega_s, c=colours[input.param()])

        ax.set_xscale("log")

        ax.set_xlabel(f"Fold change in {input.param()}")
        ax.set_ylabel(r"Fold change  $\omega_S$")

        ax.set_xlim(1e-4, 1e4)
        fig.tight_layout()
