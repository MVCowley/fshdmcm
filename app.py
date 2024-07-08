import matplotlib.pyplot as plt
import numpy as np
from shiny import render, reactive
from shiny.express import input, render, ui
import single_markov_chain

import fields

FIELDS = fields.get_field_strings()

ui.page_opts(fillable=True, title="FSHD Markov Chain Model")

with ui.sidebar():
    ui.input_selectize(
        id="param",
        label="Select x-axis parameter",
        choices=[field for field in FIELDS],
    )

    "Set other parameters"

    ui.input_slider(
        "vd",
        f"log10(Fold change in {FIELDS[0]})",
        np.log10(1e-4),
        np.log10(1e4),
        np.log10(1),
    )
    ui.input_slider(
        "d0",
        f"log10(Fold change in {FIELDS[1]})",
        np.log10(1e-4),
        np.log10(1e4),
        np.log10(1),
    )
    ui.input_slider(
        "vt",
        f"log10(Fold change in {FIELDS[2]})",
        np.log10(1e-4),
        np.log10(1e4),
        np.log10(1),
    )
    ui.input_slider(
        "td",
        f"log10(Fold change in {FIELDS[3]})",
        np.log10(1e-4),
        np.log10(1e4),
        np.log10(1),
    )
    ui.input_slider(
        "dr",
        f"log10(Fold change in {FIELDS[4]})",
        np.log10(1e-4),
        np.log10(1e4),
        np.log10(1),
    )
    ui.input_slider(
        "delta",
        f"log10(Fold change in {FIELDS[5]})",
        np.log10(1e-4),
        np.log10(1e4),
        np.log10(1),
    )
    # Reset button
    ui.input_action_button("reset", "Reset sliders")
    ui.input_dark_mode()

"Calculated myonuclear lifetime"

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

        colours = {field: f"C{n}" for n, field in enumerate(FIELDS)}

        fig, ax = plt.subplots(figsize=(3, 3))
        ax.plot(values, omega_s, c=colours[input.param()])

        ax.set_xscale("log")

        ax.set_xlabel(f"Fold change in {input.param()}")
        ax.set_ylabel("Fold change in myonuclear lifetime")

        ax.set_xlim(1e-4, 1e4)
        fig.tight_layout()


@reactive.effect
@reactive.event(input.reset)
def _():
    for param in ["vd", "d0", "vt", "td", "dr", "delta"]:
        ui.update_slider(param, value=0)
