import numpy as np
import math
import matplotlib.pyplot as plt
import pandas as pd
import argparse
import os


def one_step_simulator(n, d, curr_s, arrival_rate, b, quiet_sim=True):
    s = curr_s
    mean_rate = 1 / (arrival_rate * (1-s[b] ** d) + s[1] * n)
    time_elapsed = np.random.exponential(mean_rate)
    unif = np.random.uniform(0, 1)
    cust_served = False
    if unif < arrival_rate * mean_rate * (1-s[b] ** d):
        if not quiet_sim:
            print(f"A customer has arrived")
        arrival_unif = np.random.uniform(0, 1)
        scaled_s = s ** d
        prob_vector = (scaled_s[0:b] - scaled_s[1:b + 1]) / (1-s[b] ** d)
        for i in range(b):
            if arrival_unif < prob_vector[i]:
                s[i + 1] += 1 / n
                cust_served = True
                if not quiet_sim:
                    print(f"The customer joined a queue with length {i}")
                break
            else:
                arrival_unif = arrival_unif - prob_vector[i]
        if not quiet_sim:
            if not cust_served:
                print("The customer was not served due to limited buffer")
    else:
        service_unif = np.random.uniform(0, 1)
        shifted_s = np.concatenate((s[2:b + 1], [0]))
        prob_vector = (s[1:b + 1] - shifted_s) / s[1]
        for i in range(b):
            if service_unif < prob_vector[i]:
                s[i + 1] = s[i + 1] - 1 / n
                if not quiet_sim:
                    print(f"Queue with length {i + 1} is served")
                break
            else:
                service_unif = service_unif - prob_vector[i]
    return s, time_elapsed, cust_served


def main_loop(total_time, n, d, b, s_init, arrival_rate):
    s = s_init
    t = 0
    curr_time_window = 0
    data_dict = {}
    data_dict["curr_time"] = []
    for i in range(1, b + 1):
        data_dict[f"s_{i}"] = []
    while t <= total_time:
        u = np.random.uniform(0, 1)
        if u <= d % 1:
            curr_d = int(d) + 1
        else:
            curr_d = int(d)
        s, time_elapsed, cust_served = one_step_simulator(n, curr_d, s, arrival_rate, b)
        t = t + time_elapsed
        if t >= curr_time_window:
            data_dict['curr_time'].append(t)
            for j in range(1, b + 1):
                data_dict[f"s_{j}"].append(s[j])
            curr_time_window += 1
    return data_dict


def plotting(m, data_dict, save_fig=False, fig_name=None):
    plt.clf()
    for i in range(1, min(m + 4, b + 1)):
        plt.plot(data_dict["curr_time"], data_dict[f"s_{i}"], label=f"s_{i}")
    plt.legend()
    plt.xlabel("Time")
    plt.ylabel("Fraction of Queues")
    if not save_fig:
        plt.show()
    else:
        plt.savefig(fig_name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--n_servers', type=int, default=10 ** 4)
    parser.add_argument('-m', '--exponent_of_d', type=float, default=3)
    parser.add_argument('-g', '--gamma', type=float, default=0.2)
    args = parser.parse_args()
    input_n = args.n_servers
    input_gamma = args.gamma
    input_m = args.exponent_of_d

    input_top_level_dir = os.getcwd()

    arrival_rate = input_n - input_n ** (1 - input_gamma)

    # d = 2
    # while input_n - input_n ** (1 - input_gamma) * d ** (input_m - 1) > 0:
    #     d = d + 1
    # d = np.round(input_n ** (input_gamma / input_m), 2)
    d = 2
    while d <= (2 * input_m * input_n ** input_gamma * np.log(d)) ** (1 / input_m):
        d = d + 1
    d = min(d - 1, input_n)
    # d = int((input_n ** input_gamma) ** (1 / input_m))
    # d = input_n
    b = int(input_m) + 3

    s_init = np.zeros(b + 1)
    # for i in range(1, input_m + 1):
    #     s_init[i] = (arrival_rate / input_n) ** ((d ** i - 1) / (d - 1))
    s_init[0] = 1
    if d > 1:
        data_dict = main_loop(total_time=4000,
                            n=input_n,
                            d=d,
                            b=b,
                            s_init=s_init,
                            arrival_rate=arrival_rate
                            )
        pd_data_dict = pd.DataFrame.from_dict(data_dict)
        pd_data_dict.to_csv(f"{input_top_level_dir}/m_{input_m}_n_{input_n}_gamma_{input_gamma}_d_{d}.csv")