import os
import psutil
import time
import threading

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def find_process_by_name(process_name):
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        if proc.info['name'] == process_name:
            return proc
    return None

def print_progress_bar(process_name, date_time, cpu_percent, memory_percent, avg_cpu, avg_memory, bar_length=20):
    cpu_bar = int(cpu_percent / 5)
    memory_bar = int(memory_percent / 5)
    cpu_display = '|' + '=' * cpu_bar + ' ' * (bar_length - cpu_bar) + '|'
    memory_display = '|' + '=' * memory_bar + ' ' * (bar_length - memory_bar) + '|'
    print(f'Date: {date_time}')
    print(f'Process Name: {process_name}')
    print(f'CPU Usage: {cpu_display} {cpu_percent:.2f}%')
    print(f'Memory Usage: {memory_display} {memory_percent:.2f}%')
    print(f'Average CPU Usage: {avg_cpu:.2f}%')
    print(f'Average Memory Usage: {avg_memory:.2f}%')

def calculate_average(usage_list):
    if usage_list:
        return sum(usage_list) / len(usage_list)
    return 0

def monitor_process(process_name, interval, iterations, process_running):
    cpu_usage_list = []
    memory_usage_list = []

    while process_running.is_set() and iterations > 0:
        clear_console()
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        process = find_process_by_name(process_name)
        if process is None:
            print(f"Process '{process_name}' not found.")
            process_running.clear()
            break
        cpu_percent = process.info['cpu_percent']
        memory_percent = process.info['memory_percent']
        cpu_usage_list.append(cpu_percent)
        memory_usage_list.append(memory_percent)
        avg_cpu = calculate_average(cpu_usage_list)
        avg_memory = calculate_average(memory_usage_list)
        print("Monitoring Process:")
        print_progress_bar(process_name, current_time, cpu_percent, memory_percent, avg_cpu, avg_memory)
        iterations -= 1
        time.sleep(interval)

def main(process_name, interval, iterations):
    process_running = threading.Event()
    process_running.set()
    monitor_thread = threading.Thread(target=monitor_process, args=(process_name, interval, iterations, process_running))
    monitor_thread.start()
    try:
        monitor_thread.join()
    except KeyboardInterrupt:
        print("Process interrupted.")

if __name__ == "__main__":
    process_name = input("Enter the name of the process to attach to: ")
    interval = float(input("Enter the monitoring interval in seconds: "))
    iterations = int(input("Enter the number of iterations to calculate average: "))
    main(process_name, interval, iterations)
