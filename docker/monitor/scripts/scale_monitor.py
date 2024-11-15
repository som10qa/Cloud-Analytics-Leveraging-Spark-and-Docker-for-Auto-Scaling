import os
import subprocess
import time
import psutil  # Ensure psutil is installed via `pip install psutil`

# Constants for thresholds and scaling
CPU_UPPER_THRESHOLD = 10  # Example realistic threshold
CPU_LOWER_THRESHOLD = 5
MAX_WORKERS = 10
MIN_WORKERS = 1
SLEEP_INTERVAL = 60       # Check interval
#COOLDOWN_PERIOD = 120     # Wait time before scaling again (in seconds)
CONSECUTIVE_TRIGGER = 2   # Number of consecutive times the threshold must be met to trigger scaling

# Variables to track state
cooldown_active = False
last_scale_time = 0
upper_count = 0
lower_count = 0

def check_cpu_usage():
    return psutil.cpu_percent(interval=1)

def get_current_worker_count():
    result = subprocess.run("docker ps -q -f name=spark-worker | wc -l", shell=True, capture_output=True, text=True)
    return int(result.stdout.strip())

def scale_workers(target_scale):
    global last_scale_time, cooldown_active
    current_scale = get_current_worker_count()
    if target_scale != current_scale:
        print(f"Scaling to {target_scale} workers (current: {current_scale})...")
        cmd = f"docker-compose -f ./config/docker-compose.yml up --scale spark-worker={target_scale} -d"
        subprocess.call(cmd, shell=True)
        last_scale_time = time.time()  # Reset last scale time
        # cooldown_active = True

def auto_scale():
    global upper_count, lower_count, cooldown_active, last_scale_time
    while True:
        # if cooldown_active and (time.time() - last_scale_time < COOLDOWN_PERIOD):
        #     print(f"[INFO] Cooling down. {COOLDOWN_PERIOD - (time.time() - last_scale_time):.2f}s left.")
        #     time.sleep(SLEEP_INTERVAL)
        #     continue

        cpu_usage = check_cpu_usage()
        current_worker_count = get_current_worker_count()
        print(f"[DEBUG] CPU usage: {cpu_usage}%, Current worker count: {current_worker_count}")

        if cpu_usage > CPU_UPPER_THRESHOLD:
            upper_count += 1
            lower_count = 0
            if upper_count >= CONSECUTIVE_TRIGGER and current_worker_count < MAX_WORKERS:
                scale_workers(current_worker_count + 1)
                upper_count = 0
        elif cpu_usage < CPU_LOWER_THRESHOLD:
            lower_count += 1
            upper_count = 0
            if lower_count >= CONSECUTIVE_TRIGGER and current_worker_count > MIN_WORKERS:
                scale_workers(current_worker_count - 1)
                lower_count = 0
        else:
            upper_count = 0
            lower_count = 0

        time.sleep(SLEEP_INTERVAL)

if __name__ == "__main__":
    auto_scale()
