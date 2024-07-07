import numpy as np
import copy
import matplotlib.pyplot as plt


def gen_parameters(param_list, param, mod):
    mod_param_list = copy.copy(param_list)
    mod_param_list[param] = mod_param_list[param] * mod
    return mod_param_list


def gen_q_matrix(parameters):
    vd = parameters[0]
    d0 = parameters[1]
    vt = parameters[2]
    td = parameters[3]
    dr = parameters[4]
    delta = parameters[5]

    # Syncitial probabilities
    # S
    Pes = vd / (vd + delta)
    Prs = delta / (vd + delta)

    # E
    Pse = d0 / (d0 + td * vt + delta)
    Pie = (td * vt + delta) / (d0 + td * vt + delta)

    # I
    Pri = d0 / (d0 + dr)
    Pdi = dr / (d0 + dr)

    # R
    Pir = vd / (vd + dr)
    Pdr = dr / (vd + dr)

    Q = [[0, Pes, 0, Prs], [Pse, 0, Pie, 0], [0, 0, 0, Pri], [0, 0, Pir, 0]]

    return Q


def gen_eta(parameters):
    vd = parameters[0]
    d0 = parameters[1]
    vt = parameters[2]
    td = parameters[3]
    dr = parameters[4]
    delta = parameters[5]

    inv_eta = np.asarray([delta + vd, d0 + delta + vt * td, d0 + dr, vd + dr])

    return 1 / inv_eta


def calc_omega_s(parameters):
    a = parameters[0]  # vd
    b = parameters[1]  # d0
    c = parameters[2]  # vt
    d = parameters[3]  # td
    e = parameters[4]  # dr
    f = parameters[5]  # delta

    return (
        a * c * d
        + a * f
        + e * a
        + b * f
        + e * b
        + c * d * f
        + e * c * d
        + f**2
        + e * f
    ) / (e * (a * c * d + a * f + b * f + c * d * f + f**2))


def calc_array(
    modified_param: str, param_list: list, logmin: int, logmax: int
) -> np.array:
    param_converter = {
        "DUX4 transcription rate": 0,
        "DUX4 mRNA degredation rate": 1,
        "DUX4 target transcription rate": 2,
        "DUX4 translation rate": 3,
        "Death rate": 4,
        "DUX4 syncytial diffusion rate": 5,
    }

    base = calc_omega_s(param_list)
    values = np.logspace(logmin, logmax, 100)
    omega_s = []
    for value in values:
        params = gen_parameters(
            param_list, param_converter[modified_param], value
        )
        omega_s.append(calc_omega_s(params) / base)

    return values, omega_s
