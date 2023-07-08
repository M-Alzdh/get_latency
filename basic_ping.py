import csv
import subprocess
import time
import sys

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
    csv_file = 'ping_results_aparat.csv'  # Replace with the desired CSV file name

    timer = time.time()
    status = False
    while True:
        current_time = time.time()
        elapsed_time = current_time - timer

        if elapsed_time >= 1:
            latency_kharej = ping_ip(ip_kharej)
            latency_iran = ping_ip(ip_iran)
            time_stamp_date = time.strftime('%Y-%m-%d')
            time_stamp_hour = time.strftime('%H:%M:%S')
            write_to_csv(csv_file, [time_stamp_date, time_stamp_hour, ip_kharej, latency_kharej])
            write_to_csv(csv_file, [time_stamp_date, time_stamp_hour, ip_iran, latency_iran])
            sys.stdout.write(f"\r kharej: {latency_kharej} iran: {latency_iran}")
            sys.stdout.flush()
            timer = current_time

        time.sleep(0.05)  # Delay to avoid high CPU usage

