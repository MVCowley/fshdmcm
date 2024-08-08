import math
import numpy as np


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
    Q = gen_q_matrix(parameters)
    N = np.linalg.inv((np.identity(4) - Q))
    eta = gen_eta(parameters)
    omega = np.dot(N, eta)
    return omega[0]


def gen_two_parameters(param1, param2, mod1, mod2):
    vd = 0.00211
    d0 = 0.246
    vt = 6.41
    td = 1 / 13
    dr = 1 / 20.2
    delta = 0.04023596

    param_list = [vd, d0, vt, td, dr, delta]
    param_list[param1] = param_list[param1] * mod1
    param_list[param2] = param_list[param2] * mod2

    return param_list


def calc_pair_array(param_list) -> tuple[np.ndarray, np.ndarray]:
    # Calculate pairwise combinations
    n = len(param_list)
    k = 2
    combinations = math.factorial(n) / (
        math.factorial(k) * math.factorial(n - k)
    )

    # Create numpy array with parameter ranges
    values = np.logspace(-2, 2, 100)

    # Create object to populate with calculated absorption times
    omega_s_array = np.full(
        (int(combinations), len(values), len(values)), np.nan
    )

    # Create object to populate with pair indexes
    pair_array = np.empty(int(combinations), dtype=object)

    combination = 0
    for i in range(len(param_list)):
        for j in range(i + 1, len(param_list)):
            i_values = values
            for index0, i_value in enumerate(i_values):
                j_values = values
                for index1, j_value in enumerate(j_values):
                    params = gen_two_parameters(i, j, i_value, j_value)
                    omega_s_array[combination, index0, index1] = calc_omega_s(
                        params
                    )
            pair_array[combination] = (i, j)
            combination += 1

    return omega_s_array, pair_array


def gen_parameters(param, mod):
    vd = 0.00211
    d0 = 0.246
    vt = 6.41
    td = 1 / 13
    dr = 1 / 20.2
    delta = 0.04023596

    param_list = [vd, d0, vt, td, dr, delta]
    param_list[param] = param_list[param] * mod

    return param_list


def calc_singlet_omega_s_array(param_list):
    # Create numpy array with parameter ranges
    values = np.logspace(-2, 2, 100)

    # Create object to populate with calculated absorption times
    singlet_omega_s_array = np.full((len(param_list), len(values)), np.nan)

    for i in range(len(param_list)):
        for index, i_value in enumerate(values):
            params = gen_parameters(i, i_value)
            singlet_omega_s_array[i, index] = calc_omega_s(params)

    return singlet_omega_s_array
