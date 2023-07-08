import csv
import subprocess
import time
import sys
import concurrent.futures

def ping_ip(ip):
    try:
        output = subprocess.check_output(['ping', '-n', '1', ip], timeout=1).decode('utf-8')
        time_ms = output.split('Average = ')[1].split('ms')[0]
        return time_ms
    except Exception as e:
        print(f"{e}")
        return "0"

def write_to_csv(file_path, data):
    with open(file_path, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

if __name__ == '__main__':
    ip_kharej = '1.1.1.1'
    ip_iran = '64.98.135.91' # Aparat
    csv_file = 'ping_results_aparat.csv'

    timer = time.time()
    status = False
    while True:
        current_time = time.time()
        elapsed_time = current_time - timer

        if elapsed_time >= 1:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = [executor.submit(ping_ip, ip_kharej), executor.submit(ping_ip, ip_iran)]
                results = [future.result() for future in concurrent.futures.as_completed(futures)]

            time_stamp_date = time.strftime('%Y-%m-%d')
            time_stamp_hour = time.strftime('%H:%M:%S')
            write_to_csv(csv_file, [time_stamp_date, time_stamp_hour, results[0], results[1]])
            sys.stdout.write(f"\r {results}")
            sys.stdout.flush()
            timer = current_time

        time.sleep(0.05)
