import csv
import subprocess
import time
import sys
import concurrent.futures
import os 



def ping_ip(ip):
    try:
        output = subprocess.check_output(['ping', '-n', '1', ip], timeout=1).decode('utf-8')
        time_ms = output.split('Average = ')[1].split('ms')[0]
        return time_ms
    except Exception:
        return "0"

def create_folder(folder_path):
    try:
        os.makedirs(folder_path)
        print(f"Folder '{folder_path}' created successfully.")
    except FileExistsError:
        print(f"Folder '{folder_path}' already exists.")



def file_exists(file_path):
    try:
        with open(file_path, 'r'):
            pass
        return True
    except FileNotFoundError:
        return False

def make_file_name(data):
    last = len(data)-1
    file_path = os.path.dirname(os.path.abspath(__file__)) + "\ping_results"
    try:
        start = data[0][0]+ " @ " + data[0][1].replace(":", "-")
        end = data[last][0]+ " @ " + data[last][1].replace(":", "-")
        return file_path + "\\" + start + " _ " + end +".csv"
    except Exception as e:
        print(f"\n {e}")

def write_to_csv(file_path, data, header):
    mode = 'a' if file_exists(file_path) else 'w'
    with open(file_path, mode, newline='') as file:
        writer = csv.writer(file, delimiter=",", quoting=csv.QUOTE_NONE)
        writer.writerow(header)
        for element in data:
            writer.writerow(element)

def write_buffer(buffer, header):
            file_path_name = make_file_name(buffer) 
            write_to_csv(file_path_name,buffer, header)
            print(f"\n saved to {file_path_name}")
    


if __name__ == '__main__':
    folder_path = os.path.dirname(os.path.abspath(__file__)) + "\ping_results" 

    if not os.path.exists(folder_path):
        create_folder(folder_path)
    else:
        print(f"Folder '{folder_path}' already exists.")

if __name__ == '__main__':
    rows_per_csv = 10 # 0.5 hr per csv
    ip_kharej = '8.8.8.8'
    ip_iran = '64.98.135.91' # Aparat

    timer = time.time()
    buffer = []
    try:
        while True:
            current_time = time.time()
            elapsed_time = current_time - timer

            if elapsed_time >= 1:
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    futures = [executor.submit(ping_ip, ip_kharej), executor.submit(ping_ip, ip_iran)]
                    results = [future.result() for future in concurrent.futures.as_completed(futures)]

                time_stamp_date = time.strftime('%Y-%m-%d')
                time_stamp_hour = time.strftime('%H:%M:%S')
                buffer.append([time_stamp_date, time_stamp_hour, results[0], results[1]])
                sys.stdout.write(f"\r {results}")
                sys.stdout.flush()
                timer = current_time
            time.sleep(0.05)
            if len(buffer) >= rows_per_csv: # every 5 min
                write_buffer(buffer, header = ['date', 'time', ip_kharej, ip_iran])
                buffer = []
    except KeyboardInterrupt:
        print(f"\r Interrupted")
        if buffer:
            write_buffer(buffer,  header = ['date', 'time', ip_kharej, ip_iran])
            buffer = []
            
