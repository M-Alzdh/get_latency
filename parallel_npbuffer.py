import csv
import subprocess
import time
import sys
import concurrent.futures
import numpy as np

def ping_ip(ip):
    try:
        output = subprocess.check_output(['ping', '-n', '1', ip], timeout=1).decode('utf-8')
        time_ms = output.split('Average = ')[1].split('ms')[0]
        return time_ms
    except Exception as e:
        print(f"{e}")
        return "0"

def write_to_csv(file_path, data):
    mode = 'a' if file_exists(file_path) else 'w'
    with open(file_path, mode, newline='') as file:
        writer = csv.writer(file)
        for element in data:
            writer.writerow([element])

def file_exists(file_path):
    try:
        with open(file_path, 'r'):
            pass
        return True
    except FileNotFoundError:
        return False

def np_write(file_path, data):
    if file_exists(file_path):
         np_rbind(file_path, data)
    else:
       np.savetxt(file_path, data)


def np_rbind(file_path, data):
        np.savetxt(file_path, data, delimiter=", ", newline="\n", fmt="%s", encoding="utf-8")
         
clim = 10
counter = 0
if __name__ == '__main__':
    ip_kharej = '1.1.1.1'
    ip_iran = '64.98.135.91' # Aparat
    csv_file = 'ping_results_parallel_buffer.csv'

    timer = time.time()
while True:
    buffer = np.empty((clim, 1), dtype = "str")

    while counter < clim:
        current_time = time.time()
        elapsed_time = current_time - timer

        if elapsed_time >= 1:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = [executor.submit(ping_ip, ip_kharej), executor.submit(ping_ip, ip_iran)]
                results = [future.result() for future in concurrent.futures.as_completed(futures)]

            time_stamp_date = time.strftime('%Y-%m-%d')
            time_stamp_hour = time.strftime('%H:%M:%S')
            buffer[counter] = [time_stamp_date, time_stamp_hour, results[0], results[1]]
            sys.stdout.write(f"\r {results}")
            sys.stdout.flush()
            print(f"\n {buffer}")
            timer = current_time
        time.sleep(0.05)
        counter = counter + 1
    counter = 0
        



