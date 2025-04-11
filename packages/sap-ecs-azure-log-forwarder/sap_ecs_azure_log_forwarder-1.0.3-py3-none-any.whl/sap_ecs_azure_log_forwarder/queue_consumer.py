import time
import json
import base64
import logging
from azure.storage.queue import QueueServiceClient
from .config import (
    SAS_TOKEN,
    STORAGE_ACCOUNT_NAME,
    QUEUE_NAME,
    TIMEOUT_DURATION,
    OUTPUT_METHOD,
    HTTP_ENDPOINT,
    AUTH_METHOD,
    AUTH_TOKEN,
    API_KEY,
    OUTPUT_DIR,
    LOG_LEVEL
)
import os
from .log_processor import process_log_file

# Global Variables
MAX_RETRIES = 5  # Maximum number of retries for a message

def validate_inputs():
    errors = []

    logging.debug("-----------------------------------------\nEnivronment variables:")
    def validate_string(var_name, var_value):
        logging.debug(f"{var_name}: {var_value}")
        if not var_value or not isinstance(var_value, str) or var_value.strip() == "":
            errors.append(f"{var_name} is required and must be a non-empty string.")

    validate_string("SAS_TOKEN", SAS_TOKEN)
    validate_string("STORAGE_ACCOUNT_NAME", STORAGE_ACCOUNT_NAME)
    validate_string("QUEUE_NAME", QUEUE_NAME)
    validate_string("OUTPUT_METHOD", OUTPUT_METHOD)

    if OUTPUT_METHOD not in ["http", "files"]:
        errors.append("OUTPUT_METHOD must be either 'http' or 'files'.")

    if OUTPUT_METHOD == "http":
        validate_string("HTTP_ENDPOINT", HTTP_ENDPOINT)
        validate_string("AUTH_METHOD", AUTH_METHOD)
        if AUTH_METHOD not in ["token", "api_key"]:
            errors.append("AUTH_METHOD must be either 'token' or 'api_key' when OUTPUT_METHOD is 'http'.")
        if AUTH_METHOD == "token":
            validate_string("AUTH_TOKEN", AUTH_TOKEN)
        elif AUTH_METHOD == "api_key":
            validate_string("API_KEY", API_KEY)
    elif OUTPUT_METHOD == "files":
        validate_string("OUTPUT_DIR", OUTPUT_DIR)

    if LOG_LEVEL.upper() not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
        errors.append("LOG_LEVEL must be one of 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'.")

    if errors:
        raise ValueError("Input validation failed with the following errors:\n" + "\n".join(errors))

def is_relevant_blob_event(subject):
    """Filter relevant blob events based on the subject."""
    # Check that the subject does not contain "azure-webjobs-hosts"
    if "azure-webjobs-hosts" in subject:
        return False
    return "logserv" in subject

def set_log_level():
    """Set the log level based on the LOG_LEVEL environment variable."""
    valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
    
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    if log_level not in valid_levels:
        logging.warning(f"Invalid LOG_LEVEL '{log_level}', defaulting to INFO.")
        log_level = "INFO"

    numeric_level = getattr(logging, log_level, logging.INFO)
    
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=numeric_level,
    )
    logging.info(f"Log level set to {logging.getLevelName(numeric_level)}")

def consume_queue():
    # Set log level
    set_log_level()

    # Validate inputs before starting the queue consumer
    validate_inputs()

    DELETED_MESSAGE = "Message deleted."

    logging.info("Starting queue consumer...")
    account_url = f"https://{STORAGE_ACCOUNT_NAME}.queue.core.windows.net"
    queue_service = QueueServiceClient(account_url=account_url, credential=SAS_TOKEN)
    queue_client = queue_service.get_queue_client(QUEUE_NAME)
    
    start_time = time.time()
    try:
        while True:
            elapsed_time = time.time() - start_time
            if TIMEOUT_DURATION and elapsed_time > TIMEOUT_DURATION:
                logging.info("Timeout reached. Exiting.")
                break

            messages = queue_client.receive_messages(messages_per_page=10, visibility_timeout=5)
            if not messages:
                logging.info("No messages in the queue. Waiting...")
                time.sleep(20)  # Sleep for a while before polling again
                continue

            for message in messages:
                # Decode the Base64 message and the JSON in it.
                try:
                    decoded_message = base64.b64decode(message.content).decode('utf-8')
                    message_content = json.loads(decoded_message)
                except Exception as e:
                    logging.error(f"Failed to decode message: {e} - Message content: {message.content}")
                    queue_client.delete_message(message)
                    logging.debug(DELETED_MESSAGE)
                    continue

                # Check if the event is a relevant blob creation event
                event_type = message_content.get('eventType', '')
                subject = message_content.get('subject', '')
                if event_type != 'Microsoft.Storage.BlobCreated' or not is_relevant_blob_event(subject):
                    logging.debug(f"Irrelevant message: event_type={event_type}, subject={subject}. Skipping message.")
                    queue_client.delete_message(message)
                    logging.debug(DELETED_MESSAGE)
                    continue
                
                # Implementing a simple retry mechanism
                retry_count = int(message_content.get('retry_count', 0))
                if retry_count >= MAX_RETRIES:
                    logging.error(f"Max retries reached for message: {message.id}. Deleting message.")
                    queue_client.delete_message(message)
                    logging.debug(DELETED_MESSAGE)
                    continue

                # Extract the blob URL
                blob_url = message_content.get('data', {}).get('url', '')
                if not blob_url:
                    logging.error(f"No blob URL found in message: {message.id} - {decoded_message}")
                    queue_client.delete_message(message)
                    logging.debug(DELETED_MESSAGE)
                    continue

                try:
                    logging.info(f"Processing message: {message.id} - {blob_url}")
                    process_log_file(blob_url)
                    queue_client.delete_message(message)
                    logging.debug(DELETED_MESSAGE)
                    logging.info(f"Message processed and deleted: {message.id}")
                except Exception as e:
                    logging.error(f"Error processing message {message.id}: {e}")
                    # Increment retry count and update message
                    message_content['retry_count'] = retry_count + 1
                    updated_message = base64.b64encode(json.dumps(message_content).encode('utf-8')).decode('utf-8')
                    queue_client.update_message(message, content=updated_message, visibility_timeout=0)

    except KeyboardInterrupt:
        logging.info("Forwarder stopped by user.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    consume_queue()
