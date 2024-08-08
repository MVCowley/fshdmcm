import matplotlib.pyplot as plt
import numpy as np
from shiny import render, reactive
from shiny.express import input, render, ui
import lifetime
import interaction
import sensitivity

import fields

FIELDS = fields.get_field_strings()

ui.page_opts(fillable=True, title="FSHD Markov Chain Model")


with ui.sidebar():

    with ui.popover(id="btn_popover"):
        ui.input_action_button("btn", "Symbols", class_="mt-3")

        "V_D = DUX4 transcription rate; "
        "d_0 = DUX4 mRNA degradation rate; "
        "V_T = D4T transcription rate; "
        "T_D = DUX4 mRNA translation rate; "
        "D_r = D4T+ myonuclear apoptosis rate; "
        "Delta = DUX4 syncytial diffusion rate; "

    "Set base parameters:"

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
    ui.input_dark_mode(mode="light")

with ui.navset_card_tab(id="tab"):
    with ui.nav_panel("Lifetime"):

        with ui.card(full_screen=True):
            ui.input_selectize(
                id="param",
                label="Select x-axis parameter",
                choices=[field for field in FIELDS],
            )

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

                lifetime.plot_lifetime(input.param(), real_params)

    with ui.nav_panel("Sensitivity"):

        with ui.card(full_screen=True):

            @render.plot
            def plot_sensitivity():
                real_params = [
                    (0.00211) * 10 ** input.vd(),
                    (0.246) * 10 ** input.d0(),
                    (6.41) * 10 ** input.vt(),
                    (1 / 13) * 10 ** input.td(),
                    (1 / 20.2) * 10 ** input.dr(),
                    (0.04023596) * 10 ** input.delta(),
                ]

                sensitivity.plot_sensitivity(real_params)

    with ui.nav_panel("Interaction"):

        with ui.card(full_screen=True):
            choices = [field for field in FIELDS]
            ui.input_selectize(
                id="param1",
                label="Select first parameter",
                choices=choices,
                selected=choices[0],
            )
            ui.input_selectize(
                id="param2",
                label="Select second parameter",
                choices=choices,
                selected=choices[1],
            )

            ui.input_task_button(
                "go", "Calculate!", class_="btn-success", width="33%"
            )

            @render.plot(alt="A pair of heatmaps showing parameter interaction")
            @reactive.event(input.go, ignore_none=False, ignore_init=True)
            def interaction_plot():
                real_params = [
                    (0.00211) * 10 ** input.vd(),
                    (0.246) * 10 ** input.d0(),
                    (6.41) * 10 ** input.vt(),
                    (1 / 13) * 10 ** input.td(),
                    (1 / 20.2) * 10 ** input.dr(),
                    (0.04023596) * 10 ** input.delta(),
                ]

                interaction.interaction_plot(
                    real_params, input.param1(), input.param2()
                )

        @reactive.effect
        @reactive.event(input.reset)
        def _():
            for param in ["vd", "d0", "vt", "td", "dr", "delta"]:
                ui.update_slider(param, value=0)
