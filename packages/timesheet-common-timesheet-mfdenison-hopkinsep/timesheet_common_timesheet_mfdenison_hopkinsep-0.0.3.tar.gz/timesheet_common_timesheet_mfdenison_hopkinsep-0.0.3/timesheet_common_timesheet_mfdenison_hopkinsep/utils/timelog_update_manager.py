from ..models import TimeLog
import google.cloud.logging
import logging
from ..serializers import TimeLogSerializer

# Initialize the Google Cloud Logging client
client = google.cloud.logging.Client()
client.setup_logging()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class TimeLogUpdateManager:
    def __init__(self, timelog_id, data):
        self.timelog_id = timelog_id
        self.data = data

    def update_timelog(self):
        try:
            # Get the TimeLog object.
            timelog = TimeLog.objects.get(id=self.timelog_id)
            logger.info("Retrieved TimeLog: %s", timelog)

            numeric_fields = [
                "monday_hours",
                "tuesday_hours",
                "wednesday_hours",
                "thursday_hours",
                "friday_hours",
                "pto_hours",
            ]

            # Only include keys that correspond to fields on the model.
            valid_data = {}
            for key, value in self.data.items():
                if hasattr(timelog, key):
                    if value is None:
                        logger.info("Field '%s' is None; setting to 0", key)
                        valid_data[key] = 0
                    else:
                        # If this field is numeric, try to convert to int.
                        if key in numeric_fields:
                            try:
                                valid_data[key] = int(value)
                            except Exception as conv_error:
                                logger.warning("Failed to convert field '%s' value %s to int: %s. Setting to 0.", key, value, conv_error)
                                valid_data[key] = 0
                        else:
                            valid_data[key] = value
                else:
                    logger.warning("Field '%s' not found on TimeLog model; skipping", key)

            logger.info("Filtered update data: %s", valid_data)

            # Use the serializer with partial=True to update only provided fields.
            serializer = TimeLogSerializer(timelog, data=valid_data, partial=True)
            if not serializer.is_valid():
                logger.error("Validation errors: %s", serializer.errors)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            logger.info("TimeLog updated successfully with id %s", self.timelog_id)
            return {"result": "success"}
        except TimeLog.DoesNotExist:
            error_message = f"TimeLog with id:{self.timelog_id} does not exist."
            logger.error(error_message)
            return {"result": "failure", "message": error_message}
        except Exception as e:
            logger.exception("Exception in update_timelog:")
            return {"result": "failure", "message": str(e)}

