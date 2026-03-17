# Self-Healing_Nginx
Used monitoring tools to check nginx and start/restart nginx if it is down.

## 📌 Project Overview

This project demonstrates a complete monitoring and auto-remediation pipeline for an NGINX server using:

* **Prometheus** for metrics collection
* **Alertmanager** for alert handling
* **NGINX** with `stub_status` enabled for monitoring
* **Webhook Receiver** for alert ingestion
* **Automation Playbook (Ansible)** for self-healing

The system automatically detects when NGINX goes down and triggers a recovery mechanism.

---

## 🏗️ Architecture

```
NGINX → Prometheus → Alert Rules → Alertmanager → Webhook → Automation Playbook → NGINX Restart
```

---

## 🧰 Tech Stack

This project leverages the following tools and technologies:

* **NGINX** – Web server being monitored
* **NGINX Prometheus Exporter** – Exposes NGINX metrics in Prometheus format
* **Prometheus** – Metrics collection and monitoring system
* **Alertmanager** – Handles alerts and routes them to external systems
* **Webhook Receiver (Flask App)** – Receives alerts and triggers automation
* **Ansible** – Automation tool used to restart NGINX (self-healing)

---

## 🔗 How They Work Together

* **NGINX + Exporter** → Generate and expose metrics
* **Prometheus** → Scrapes metrics from exporter
* **Alertmanager** → Sends alerts when rules are triggered
* **Flask Webhook** → Receives alert payload
* **Ansible Playbook** → Executes recovery action

---

## ⚙️ Setup Steps

### 1️⃣ Configure NGINX Metrics

* Enable the `stub_status` module in your NGINX configuration.
* Expose a status endpoint (e.g., `/nginx_status`) on a specific port.
* Ensure that the endpoint is accessible to the Prometheus container.
* Verify access by visiting the status URL in a browser.

---

### 2️⃣ Use Docker Compose to Start Services

* Docker-Compose file includes:

  * Prometheus
  * NGINX Exporter
  * Alertmanager
* Ensure all services are on the same network so they can communicate.
* Start the stack using:

  ```bash
  docker-compose up -d
  ```

---

### 3️⃣ Configure Prometheus Scraping

* Configure Prometheus to scrape metrics from the NGINX exporter.
* Ensure the correct target (exporter service name and port) is used.
* Verify that Prometheus is successfully collecting metrics by checking its UI.

---

### 4️⃣ Define Alert Rules

* Create an alert rule that triggers when the NGINX target is down.
* Use a condition like `up == 0` for the NGINX job.
* Set a duration (e.g., 1 minute) before firing the alert to avoid false positives.

---

### 5️⃣ Configure Alertmanager

* Set up Alertmanager to receive alerts from Prometheus.
* Define a route that sends alerts to a webhook receiver.
* Ensure the webhook endpoint is reachable from the Alertmanager container.

---

### 6️⃣ Set Up Webhook Receiver

* Use webhook-reciever.py to start a FLASK application.
* It will parse the webhook and Triggers an ansible playbook that starts NGINX.
* Run the FLASK app using `pyhton webhook_reciever.py`.
> Note: Run the app as a root user because to run ansible playbook root access is required; Otherwise ansible playbook asks for password due to which automation may be interrupted.

---

### 7️⃣ Automate Recovery with Ansible

* Use Automation.yml (Ansible playbook) to restart the NGINX service.
* Ensure the webhook receiver can execute the playbook.
* Test the automation by manually stopping NGINX and verifying it restarts automatically.

---

## 🔄 Workflow

1. Prometheus scrapes NGINX metrics
2. If NGINX is down → `up == 0` triggers alert
3. Alert is sent to Alertmanager
4. Alertmanager sends webhook
5. Webhook receiver executes Ansible playbook
6. NGINX service is restarted automatically

---

## ✅ Key Features

* 📊 Real-time monitoring
* 🚨 Automated alerting
* 🔁 Self-healing infrastructure
* 🔗 Webhook-based integration
* ⚡ Lightweight and extensible

---

## 🛠️ Prerequisites

* NGINX installed
* Prometheus installed
* Alertmanager installed
* Python (for webhook receiver)
* Ansible installed

---

## ▶️ How to Run

1. Start NGINX with `stub_status` enabled
2. Start Prometheus and Alertmanager:

   ```bash
   docker-compose up -d
   ```
4. Run webhook receiver:

   ```bash
   python webhook_reciever.py
   ```
5. Stop NGINX manually to test:

   ```bash
   systemctl stop nginx
   ```

✔️ Alert will trigger → Playbook will run → NGINX will restart

---

## 📌 Future Enhancements

* Add Slack/Email notifications
* Use exporters like `nginx-prometheus-exporter`
* Deploy using Docker/Kubernetes
* Add logging and observability stack (ELK/Grafana)

---

## 👨‍💻 Author

Omkar Nampalli
