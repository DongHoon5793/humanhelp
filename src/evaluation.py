from scipy.optimize import curve_fit
from sklearn.exceptions import ConvergenceWarning

import warnings
import time

warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=ConvergenceWarning)


def clustering_evaluation(clustering_algorithm, filtered_data):
    data_size_list = []
    time_list = []

    i = 1
    while True:
        data_size = pow(i, 2) * 10
        data_size_list.append(data_size)
        sample_data = filtered_data.sample(n=data_size)
        start_time = time.time()
        clustering_algorithm.fit_predict(sample_data)
        time_need = time.time() - start_time
        time_list.append(time_need)
        i += 1
        if time_need > 1.0:
            break

    def func(in_data_size, coefficient, n):
        return coefficient * pow(in_data_size, n)

    popt, pocv = curve_fit(func, data_size_list, time_list)

    expectation_time = func(len(filtered_data), *popt)

    # seconds to min + hours
    mm, ss = divmod(expectation_time, 60)
    hh, mm = divmod(mm, 60)

    print(f'To clusterize with all dataset, it needs {hh:.0f} hours {mm:.0f} minutes {ss:.1f} seconds')

    return expectation_time
