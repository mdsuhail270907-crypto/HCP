import requests
import time
import os
import sys
import io

# Force UTF-8 encoding for terminal output to support emojis
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

API_BASE = "http://127.0.0.1:5000/api"

def clear_screen():
    # Clear screen for Windows or Linux/Mac
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    while True:
        try:
            # Fetch Global Stats
            stats_resp = requests.get(f"{API_BASE}/stats", timeout=2)
            stats_resp.raise_for_status()
            stats = stats_resp.json()
            
            # Fetch Jobs to list out current activity
            jobs_resp = requests.get(f"{API_BASE}/jobs", timeout=2)
            jobs_resp.raise_for_status()
            jobs = jobs_resp.json()
            
            # Calculate active jobs
            active_jobs = [j for j in jobs if j['status'] in ['RUNNING', 'BURST_RUNNING']]
            local_jobs = len([j for j in active_jobs if j['node_type'] == 'LOCAL'])
            cloud_jobs = len([j for j in active_jobs if j['node_type'] == 'CLOUD_BURST'])
            local_cap = stats.get('local_capacity', 2)

            # Draw Terminal UI
            clear_screen()
            print("=" * 60)
            print(" 📡 HPC CLOUD BURST - TERMINAL MONITOR")
            print("=" * 60)
            print("")
            
            # Capacity Bar
            local_fill = "█" * local_jobs + "░" * max(0, local_cap - local_jobs)
            print(f" [LOCAL CLUSTER]  [{local_fill}] {local_jobs}/{local_cap} Nodes Active")
            
            if cloud_jobs > 0:
                print(f" [CLOUD BURST]    [{'⚡' * cloud_jobs}] {cloud_jobs} Container(s) Running!")
            else:
                print(f" [CLOUD BURST]    [ Idle ]")
                
            print(f"\n Total Computations: {stats.get('total', 0)} | Accumulated Cost: ${stats.get('total_cost', 0):.2f}")
            print("-" * 60)
            
            # Status Tracker
            if len(active_jobs) == 0:
                print(" No active workloads. Waiting for payloads...")
            else:
                print(f" {'ID':<10} | {'PAYLOAD':<20} | {'NODE ALLOCATION':<15} | {'STATUS'}")
                print("-" * 60)
                for job in active_jobs:
                    node_icon = "☁️" if job['node_type'] == "CLOUD_BURST" else "🖥️"
                    print(f" #{job['id']:<8} | {job['name'][:18]:<20} | {node_icon} {job['node_type']:<12} | {job['status']}")
            
            print("\n(Press CTRL+C to exit...)")
            
        except requests.exceptions.ConnectionError:
            clear_screen()
            print("=" * 60)
            print(" 📡 HPC CLOUD BURST - OFFLINE")
            print("=" * 60)
            print("\n[ERROR] Unable to connect to Backend Server.")
            print("Please ensure 'python -m backend.app' is running.")
            print("\nRetrying in 2 seconds...")
        except Exception as e:
            print(f"\n[ERROR] Monitor exception: {e}")
            
        time.sleep(1.5) # Refresh rate

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear_screen()
        print("Terminal Monitor exited cleanly.\n")
        sys.exit(0)
