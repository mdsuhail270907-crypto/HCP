# HPC Cloud Burst Platform ⚡☁️

A full-stack, enterprise-grade simulation of an **On-Premise High-Performance Computing (HPC) cluster** that automatically and elastically scales workloads into the cloud via dynamic Docker containerization when local hardware capacity is exhausted. 

Designed and engineered for high-impact hackathon demonstrations.

---

## 🛑 Problem Statement
Research institutions, AI labs, and financial modelers rely on on-premise hardware clusters (managed by systems like Slurm) to run computational workloads. However, hardware is static. 

When demand spikes (e.g., ahead of a conference deadline), local queues fill up, forcing researchers to wait hours or days for compute time. Purchasing and maintaining additional hardware just for peak traffic is wildly expensive and deeply inefficient.

## 💡 Solution Overview
**Cloud Bursting** is the holy grail of modern HPC infrastructure. 

The HPC Cloud Burst Platform solves the scaling problem by acting as an intelligent bridge between static hardware and the elastic cloud. It keeps standard, baseline workloads on cheap local hardware. However, the moment a traffic spike occurs, the platform automatically detects the bottleneck and dynamically provisions temporary Cloud virtual machines to handle the overflow, scaling back down to entirely zero when the queue clears to prevent billing overrun.

---

## 🏗️ Architecture Explanation

The project bridges a decoupled web interface with a deep system-level automation controller:

*   **Frontend (React + Vite)**: A premium "Deep Theme" SaaS dashboard. It features strict access controls, high-frequency state polling, real-time financial tracking, and a terminal output viewer to inspect artifact generation.
*   **API Router (Flask)**: The lightweight gateway that ingests multipart uploads, routes scripts, and surfaces the current cluster topography.
*   **The Orchestrator Daemon (Python)**: A multi-threaded orchestrator running constantly in the background. It polls an internal `job_queue` (which supports high/normal Priority lanes) and tracks active local allocations against the absolute internal ceiling.
*   **Cloud Execution Layer (Docker native)**: An implementation using Python's `subprocess` framework. When a cloud event is triggered, it literally reaches out to your Docker daemon to provision a fresh, isolated `python-alpine` container, pushes in your Python script, captures the physical STDOUT processing logs, and securely eradicates the container.

---

## ⚙️ How Cloud Bursting Works

1.  **Ingestion**: A user submits a computational payload via the React UI or using the raw CLI tool (`submit_job.py`).
2.  **Capacity Validation**: The Orchestrator intercepts the job and polls `monitor.py` for localized availability.
3.  **The Fork**:
    *   If `running_local_count < local_capacity (2)`: The payload is processed gracefully on the simulated "Local Node". Cost: **$0.00**.
    *   If `running_local_count >= local_capacity`: The Orchestrator locks into **Burst Mode**.
4.  **Burst Execution**: 
    *   `cloud/provision.py` spawns a Docker container.
    *   `cloud/execute.py` physical copies the script inside using `docker cp`, mounts `docker exec`, and grabs the terminal logs.
    *   `cloud/cleanup.py` executes `docker rm -f` to aggressively kill the instance.
5.  **Cost Accounting**: The length of the containerized execution is multiplied by the dynamic cloud-compute rate ($0.05/sec) and synced to the Financial Dashboard.

---

## 💻 Setup Instructions

**Prerequisites:** Node.js (18+), Python (3.10+), and [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Must be actively running for container simulations).

### 1. Backend Initialization
Open a terminal in the root directory:
```bash
# Install dependencies
pip install -r requirements.txt

# Boot the API Router AND Orchestrator threads
python -m backend.app
```

### 2. Frontend Initialization
Open a separate terminal:
```bash
cd frontend
npm install
npm run dev
```
Navigate to **`http://localhost:5173`** and create any dummy account to bypass auth and begin.

---

## 🎬 Demo Steps

To successfully wow the judges, follow this step-by-step narrative:

1.  **The Local Baseline**: 
    *   Navigate to the **Submit** tab.
    *   Rapidly click a "Quick Start Configuration" (e.g., Genome Analysis) and hit *Submit* **two times** in a row.
    *   **Dashboard Check**: Point out that the "Active Local Jobs" counter is 2, and the "Total Cloud Spend" is locked at $0.00. The system is operating normally within its physical limits.
2.  **The Spike (Triggering Burst)**: 
    *   While the first two jobs are processing, submit a **third job**. 
    *   *Optional*: In the command line, observe the Orchestrator log `[INFO] Local cluster full... Triggering cloud burst for Job...`
3.  **The Verification**: 
    *   Immediately click to your **Monitor** tab. 
    *   Show that Jobs 1 & 2 are mapped statically to `LOCAL_NODE` (🖥️), but Job 3 has instantly triggered elastic scaling and is tagged dynamically as `CLOUD_BURST` (☁️⚡).
4.  **Dynamic Costing & Artifacts**:
    *   Navigate back to the **Dashboard** and show that the "Total Cloud Spend" has accrued a micro-transaction amount (e.g., $0.50). 
    *   Finally, jump to the **Results** tab and click **Inspect** on the Burst job to prove that the heavy lifting was legitimately executed in a physically isolated container by showcasing the standard output logs.
