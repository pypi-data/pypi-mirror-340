import json
import logging
from google.cloud import pubsub_v1

# Initialize Pub/Sub client
publisher = pubsub_v1.PublisherClient()

# GCP Pub/Sub topic name (replace with your actual topic name)
dashboard_topic = 'projects/hopkinstimesheetproj/topics/dashboard-queue'

# Set up logging
logger = logging.getLogger(__name__)

def send_dashboard_update(employee_id, payload_type, data):
    """Helper to emit consistent dashboard messages."""
    try:
        # Prepare the message
        message = {
            "employee_id": employee_id,
            "type": payload_type,
            "payload": data
        }

        # Publish the message to the GCP Pub/Sub topic
        publisher.publish(
            f'projects/hopkinstimesheetproj/topics/dashboard-queue',
            data=json.dumps(message).encode('utf-8')
        )

        logger.info(f"Sent dashboard update for employee {employee_id} with type {payload_type}")

    except Exception as e:
        logger.exception(f"Failed to send dashboard update: {e}")
