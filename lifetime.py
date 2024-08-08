import analytical
import fields
import matplotlib.pyplot as plt


def plot_lifetime(input_param, real_params):
    values, omega_s = analytical.calc_array(input_param, real_params)

    colours = {
        field: f"C{n}" for n, field in enumerate(fields.get_field_strings())
    }

    ax: plt.Axes
    fig, ax = plt.subplots()
    ax.plot(values, omega_s, c=colours[input_param])

    ax.set_xscale("log")

    ax.set_xlabel(f"Fold change in {input_param}")
    ax.set_ylabel("Fold change in myonuclear lifetime")

    ax.set_xlim(1e-4, 1e4)
    fig.tight_layout()
