import string
import multiprocessing
from hashlib import sha256
import itertools
import time

with open("sha256.txt") as file:
    all_sha256 = [line.strip() for line in file]


def get_num_of_processes():
    while True:
        try:
            n = int(input("Укажите количество потоков в диапазоне от 1 до 26: "))
            if 1 <= n <= 26:
                return n
            print("Введённое число должно быть от 1 до 26")
        except ValueError:
            print("Не верный формат числа. Попробуйте снова.")

def brute(first_symbol):
    data = string.ascii_lowercase
    for x in itertools.product(first_symbol, data, data, data, data):
        sha_code = sha256(''.join(x).encode('utf-8')).hexdigest()
        if sha_code in all_sha256:
            print(multiprocessing.current_process().name, end="\t")
            print(f"Пароль {''.join(x)} - sha256:{sha_code}")


def main():
    processes = []
    num_of_processes = get_num_of_processes()
    part_process = len(string.ascii_lowercase) // num_of_processes

    start_time = time.perf_counter()

    for np in range(num_of_processes):
        if np == num_of_processes - 1:
            first_symbol = string.ascii_lowercase[part_process * np :]
        else:
            first_symbol = string.ascii_lowercase[part_process * np : part_process * (np+1)]
        proc = multiprocessing.Process(target=brute, args=(first_symbol,))
        proc.start()
        processes.append(proc)
    
    for proc in processes:
        proc.join()
        

    end_time = time.perf_counter()

    work_time = end_time-start_time
    print(f"Было использовано {num_of_processes} потоков. Время выполнения - {work_time} секунд.")

if __name__ == "__main__":
    main()