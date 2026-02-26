from flask import Flask, request, jsonify
import subprocess
import logging
import os

app = Flask(__name__)

LOG_FILE = "/home/naruto/monitoring/automation.log"

# Ensure directory exists
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

ANSIBLE_PLAYBOOK = "/home/naruto/monitoring/automation.yml"
INVENTORY = "/home/naruto/monitoring/hosts"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json

    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    alerts = data.get("alerts", [])

    for alert in alerts:
        alertname = alert.get("labels", {}).get("alertname")
        status = alert.get("status")
        instance = alert.get("labels", {}).get("instance")

        logging.info(f"Alert: {alertname}, Status: {status}")

        if alertname == "nginx-stopped" and status == "firing":
            logging.info(f"Alert received for {instance}")

            try:
                result = subprocess.run(
                    [
                        "ansible-playbook",
                        "-i", INVENTORY,
                        ANSIBLE_PLAYBOOK
                    ],
                    capture_output=True,
                    text=True,
                    check=True
                )

                logging.info("===== SUCCESS =====")
                logging.info(result.stdout)
                logging.info("===== END =====")

                return jsonify({"message": "Playbook executed"}), 200

            except subprocess.CalledProcessError as e:
                logging.error("===== FAILED =====")
                logging.error(e.stdout)
                logging.error(e.stderr)
                logging.error("===== END =====")

                return jsonify({"error": "Playbook failed"}), 500

    return jsonify({"message": "No matching alerts"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
