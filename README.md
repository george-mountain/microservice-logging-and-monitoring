# Microservice Logging and Monitoring

## Project Overview

This project demonstrates monitoring for microservices applications and servers using **Grafana**, **Loki**, **Prometheus**, **Alertmanager**, **Promtail**, and **Uptime Kuma**. The setup includes a sample FastAPI and Django service, monitored for uptime, performance, and error rates. Logs are collected and visualized using Loki and Grafana, while Prometheus and Alertmanager handle metrics and alerting.

## Setup Instructions

### Step 1: Create a `.env` File

Create a `.env` file in the root directory of the project and configure it with the necessary environment variables. Use the provided `.env-sample` as a reference by copying its contents to `.env` and updating the values as needed.

Example `.env` file:

```env
# Image names
PROMETHEUS_IMAGE=prom/prometheus:latest
NODE_EXPORTER_IMAGE=prom/node-exporter:latest
ALERTMANAGER_IMAGE=prom/alertmanager:v0.23.0
GRAFANA_IMAGE=grafana/grafana:11.2.0
UPTIME_KUMA_IMAGE=louislam/uptime-kuma:nightly2
MYSQL_IMAGE=mysql:8
LOKI_IMAGE=grafana/loki:2.9.0
PROMTAIL_IMAGE=grafana/promtail:2.9.0

# Port numbers
PROMETHEUS_PORT=9090
NODE_EXPORTER_PORT=9100
ALERTMANAGER_PORT=9093
GRAFANA_PORT=3000
UPTIME_KUMA_PORT=3001
MYSQL_PORT=3306
FASTAPI_PORT=8000
DJANGO_PORT=8001
LOKI_PORT=3100

# MySQL credentials
MYSQL_ROOT_PASSWORD=root
MYSQL_DATABASE=uptime_kuma
MYSQL_USER=uptime_kuma
MYSQL_PASSWORD=uptime_kuma

# Grafana credentials
GF_SECURITY_ADMIN_PASSWORD=admin
GF_AUTH_ANONYMOUS_ENABLED=true
```

### Step 2: Run the Application

Build and run the application using Docker Compose:

```sh
docker compose up -d --build
```

### Step 3: Access the Services

- **Django Service**: [http://localhost:8001](http://localhost:8001)
- **FastAPI Service**: [http://localhost:8000](http://localhost:8000)
- **Grafana**: [http://localhost:3000](http://localhost:3000)
- **Alertmanager**: [http://localhost:9093](http://localhost:9093)
- **Prometheus**: [http://localhost:9090](http://localhost:9090)
- **Uptime Kuma**: [http://localhost:3001](http://localhost:3001)

### Step 4: Test the Logging

Generate logs by accessing the sample FastAPI and Django API endpoints:

- **FastAPI Endpoint**: [http://localhost:8000/items/](http://localhost:8000/items/)
- **Django Endpoint**: [http://localhost:8001/api/items/](http://localhost:8001/api/items/)

Logs from these endpoints are captured by Prometheus and Loki, ready for visualization in Grafana.

### Step 5: Set Up Grafana Visualizations

Import Grafana dashboards from the `dashboard-examples` folder:

- **Node Exporter.json**: Visualizes Node Exporter metrics from Prometheus.
- **microservices_monitoring.json**: Monitors Django and FastAPI logs from Loki.

#### Importing Dashboards

1. Open Grafana ([http://localhost:3000](http://localhost:3000)).
2. Log in (default username and password: `admin`).
3. Click "+" on the left sidebar and select "Import."
4. Upload the JSON files from `dashboard-examples`.
5. Assign appropriate data sources (Prometheus for the Node Exporter.json and Loki for the microservices_monitoring.json ) to each dashboard.

### Step 6: Configure Email Notifications in Alertmanager

Edit the `alertmanager.yml` file in the `config/alertmanager` folder to set up email notifications. Replace the sample configuration with your email credentials:

```yaml
global:
  resolve_timeout: 1m

route:
  receiver: 'email-notifications'

receivers:
- name: 'email-notifications'
  email_configs:
    - to: 'youremail@gmail.com'        # Your email address
      from: 'youremail@gmail.com'      # Your email address
      smarthost: 'smtp.gmail.com:587'
      auth_username: 'youremail@gmail.com' # Your email address
      auth_password: 'yourgmailapppassword' # Gmail app password
      send_resolved: true
```

### Step 7: Add Services to Monitor in Uptime Kuma

1. Open Uptime Kuma ([http://localhost:3001](http://localhost:3001)).
2. Log in and click "Add New Monitor" on the dashboard.
3. Add FastAPI and Django services:
   - **Monitor Type**: HTTP(s)
   - **Friendly Name**: FastAPI Service
   - **URL**: `http://fastapi-service:8000`
   - **Method**: GET
   - **Interval**: 60 seconds
4. Repeat for the Django service:
   - **Monitor Type**: HTTP(s)
   - **Friendly Name**: Django Service
   - **URL**: `http://django-service:8001`
   - **Method**: GET
   - **Interval**: 60 seconds

### Additional Resources

For more detailed information on configuring notifications and monitoring in Uptime Kuma, refer to the following resource [Uptime Kuma Configuration Guide](https://betterstack.com/community/guides/monitoring/uptime-kuma-guide/).

Following these steps will enable comprehensive logging, monitoring, and alerting for your microservices application using Grafana, Loki, Prometheus, Alertmanager, Promtail, and Uptime Kuma.