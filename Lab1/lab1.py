import pandas as pd
import numpy as np
from multiprocessing import Pool
import os

MAX_FILE_LEN = 20


def file_generation():
    os.makedirs("data", exist_ok=True)

    letters = pd.Series(['A', 'B', 'C', 'D'])

    for i in range(5):
        file_path = f'data/data_{i}.csv'
        file_size = np.random.randint(2, MAX_FILE_LEN)

        categories = letters.sample(file_size, replace=True).values
        values = np.random.sample(file_size)

        data = pd.DataFrame({'category': categories, 'value': values})
        data.to_csv(file_path, index=False)


def one_process_execution(file_path):
    df = pd.read_csv(file_path)
    return df.groupby('category').agg({'value': ['mean', 'std']}).value.fillna(0)


def print_results(result_1, result_2):
    for i in range(5):
        print(f"\nМедиана и стандартное отклонение {i + 1} файла")
        print(result_1[i])
    print("\n\nМедиана и стандартное отклонение медиан из всех файлов")
    print(result_2)


if __name__ == "__main__":
    file_generation()

    file_paths = [f'data/data_{i}.csv' for i in range(5)]

    with Pool(processes=5) as pool:
        jobs = [pool.apply_async(one_process_execution, args=(file_path,)) for file_path in file_paths]
        results = [job.get() for job in jobs]

    general_mean_info= pd.concat(results).groupby('category').agg({'mean': ['std', 'mean']})
    print_results(results, general_mean_info)