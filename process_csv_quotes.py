import os
import csv

def process_csv_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            file_path = os.path.join(directory, filename)
            process_csv_file(file_path)
            print(f"processed {filename}")

def process_csv_file(file_path):
    new_lines = ["date, time, 1.1.1.1, 64.98.135.91"]
    with open(file_path, 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            for cell in row:
                new_row = cell.replace('"', '').replace("'", '').replace('[', '').replace(']', '') 
                new_lines.append(new_row)

    with open(file_path, 'w', newline='\n') as file:
        for item in new_lines:
            file.write(str(item) + "\n")
        

if __name__ == '__main__':
    directory = r'C:\Users\Haji\Documents\spotify_with_py\spotify_with_py\results'  # Replace with the directory containing the CSV files
    process_csv_files(directory)
