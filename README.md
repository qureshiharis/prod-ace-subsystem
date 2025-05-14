# ACE CyberSafe Subsystem – Raspberry Pi + Avassa Deployment

This repository contains the source code and instructions to deploy a real-time HVAC subsystem for smart building environments using **Raspberry Pi**, **Docker**, and **Avassa Edge Orchestrator**. The system supports multiple subsystems (e.g., heating, ventilation) running in parallel on one or more Raspberry Pi devices.

👉 **Docker Image Available**:  
https://hub.docker.com/r/topnot/prod-ace-subsystem
---

## 🛠️ Project Overview

This docker image allows each container in a Pi to:

- Collect sensor data via WebPort API.
- Publish the sensor data information using Avassa's built in Volga Pub/Sub method.

---

## 🔧 Prerequisites

- Raspberry Pi 5 with Raspberry Pi OS installed.
- SSH access to the Pi.
- Docker and Avassa Edge Enforcer installed on the Pi.
- Avassa Control Tower access.
- Code pushed to a container registry (already available at DockerHub).

---

## 📦 Project Structure

```bash
├── main.py              # Entry point – fetches data and runs pipeline
├── fetcher.py           # Handles WebPort data collection
├── config.py            # Reads environment configs (e.g., TAG_PAIRS, API_KEY)
├── logger_config.py     # Sets up consistent logging (timezone-aware)
├── Dockerfile           # Container build file for deployment
├── requirements.txt     # Python dependencies
├── yaml/                # Sample Avassa application configuration (YAML)
```

---

## 📦 Steps to Deploy on a New Raspberry Pi (as a Subsystem)

### 1. Install Docker and Avassa Edge Enforcer on Raspberry Pi

SSH into your Pi and run:

```bash
# Install Docker
curl -fsSL https://get.docker.com | sh

# (Optional) Add your user to the docker group
sudo usermod -aG docker $USER
```

Then onboard the Pi to your Avassa site using the **Edge Enforcer onboarding command** from Control Tower.

> Make sure to give the host a unique **host ID** and **hostname** to avoid replacement of previous hosts.

---

### 2. Use the Prebuilt Docker Image

The Docker image is already available:

```bash
docker pull topnot/prod-ace-subsystem:v1.3
```

> No need to build locally unless you modify the code. Since you need then to configure .env file 

---

### 3. Create a Site and Application in Avassa

- Create or reuse a site in Control Tower.
- Add the new Raspberry Pi as a **new host** under the same site.
- Create a new **Application** (e.g., `ace-ventilation` or `ace-heating`).

---

### 4. Prepare Your Avassa Application YAML

Here’s a sample application YAML configuration:

```yaml
name: ace-district-heating-1473
version: "1.4"
services:
  - name: district-heating-1473
    mode: replicated
    replicas: 1
    placement:
      match-host-labels: function = heating
    share-pid-namespace: false
    containers:
      - name: district-heating-v-container
        mounts: []
        container-log-size: 100 MB
        container-log-archive: false
        shutdown-timeout: 10s
        image: index.docker.io/topnot/prod-ace-subsystem:v1.3
        env:
          VOLGA_TOPIC: anomalies-heating
          USE_GPIO: "false"
          TAG_PAIRS: TAG PAIRS IN COMMA SEPARATED FORMAT
          SECRET_ID: ${SYS_APPROLE_SECRET_ID}
          ROLE_ID: YOUR_ROLE_ID
          OUTPUT_FILE: heating
          LED_PIN: "18"
          FIXED_OFFSET: +02:00
          FETCH_INTERVAL: "300"
          BUZZER_PIN: "23"
          BUFFER_HOURS: "4"
          BASE_URL: YOUR_API_URL
          API_KEY: YOUR_API_KEY
          API_CA_CERT: ${SYS_API_CA_CERT}
          ANOMALY_STD_MULTIPLIER: "3"
        approle: ace-anomaly-approle
        on-mounted-file-change:
          restart: true
    network:
      outbound-access:
        allow-all: true
on-mutable-variable-change: restart-service-instance

```

---

### 5. Deploy the Application

- Upload the YAML in the application section of Avassa.
- Deploy it to your new Pi host.
- Watch the logs to verify that the subsystem is running correctly.

---

## ✅ Troubleshooting

- If Avassa replaces your previous host, ensure you set a **unique host ID and name** during onboarding.
- If WebPort API calls fail, check that the Raspberry Pi is connected to a working network (e.g., your university Wi-Fi may block some outbound traffic).