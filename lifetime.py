import analytical
import fields
import matplotlib.pyplot as plt


def plot_lifetime(input_param, real_params):
    values, omega_s = analytical.calc_array(input_param, real_params, -4, 4)

    colours = {
        field: f"C{n}" for n, field in enumerate(fields.get_field_strings())
    }

    ax: plt.Axes
    fig, ax = plt.subplots(figsize=(3, 3))
    ax.plot(values, omega_s, c=colours[input_param])

    ax.set_xscale("log")

    ax.set_xlabel(f"Fold change in {input_param}")
    ax.set_ylabel("Fold change in myonuclear lifetime")

    ax.set_xlim(1e-4, 1e4)
    ax.set_box_aspect(1)
    fig.tight_layout()
