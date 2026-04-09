import requests
import time
import os
import getpass

API_BASE = "http://127.0.0.1:5000/api"

def print_header(title):
    print("\n" + "=" * 50)
    print(f" {title}")
    print("=" * 50)

def main():
    print_header("HPC CLI: Job Submission Tool")
    
    # 1. Gather Information
    job_name = input("Enter your Job Title > ").strip()
    if not job_name:
        job_name = "CLI-Dispatched-Workload"
        
    script_path = input("Enter path to Python script (or press Enter for Standard Template) > ").strip()
    priority = input("Priority (normal/high) [normal] > ").strip().lower()
    if priority not in ['normal', 'high']:
        priority = "normal"
        
    user_id = "cli-user-1234" # Mock user identifier for CLI

    print("\n[INFO] Packaging payload and contacting cluster...")
    
    # 2. Submit the Job
    payload = {
        'name': job_name,
        'user_id': user_id,
        'priority': priority
    }
    
    try:
        if script_path and os.path.exists(script_path):
            with open(script_path, 'rb') as f:
                files = {'file': f}
                resp = requests.post(f"{API_BASE}/jobs", data=payload, files=files)
        else:
            if script_path:
                print(f"[WARNING] Could not find {script_path}. Using standard template.")
            # JSON format if no file
            resp = requests.post(f"{API_BASE}/jobs", json=payload)
            
        resp.raise_for_status()
        job_data = resp.json()
        job_id = job_data['id']
        
        print(f"[SUCCESS] Payload accepted. Assigned Job ID: #{job_id}")
        print("\n[INFO] Waiting for allocation from Burst Controller...")
        
        # 3. Poll for Allocation Status
        allocated = False
        attempts = 0
        while not allocated and attempts < 10:
            time.sleep(1)
            status_resp = requests.get(f"{API_BASE}/jobs?user_id={user_id}")
            if status_resp.ok:
                jobs = status_resp.json()
                current_job = next((j for j in jobs if j['id'] == job_id), None)
                if current_job and current_job['node_type'] != 'PENDING':
                    node_type = current_job['node_type']
                    
                    if node_type == "LOCAL":
                        print(f"\n✅ VERDICT: Local capacity available.")
                        print(f"   Executing deeply on internal node: 🖥️ LOCAL_CLUSTER")
                    elif node_type == "CLOUD_BURST":
                        print(f"\n⚡ VERDICT: Local cluster full!")
                        print(f"   Burst active. Offloading to containerized instance: ☁️ CLOUD_DOCKER")
                    
                    allocated = True
            attempts += 1
            
        if not allocated:
            print(f"\n[WARNING] Job queued, but cluster allocation is taking longer than expected.")

    except requests.exceptions.ConnectionError:
        print("\n[ERROR] Could not connect to HPC Platform. Ensure 'python -m backend.app' is running.")
    except Exception as e:
        print(f"\n[ERROR] An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
