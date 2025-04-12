import zmq
import json
import time
import threading
from typing import Dict, Any, Optional, Callable, Tuple
import logging
import argparse
import os
import getpass
import socket
import traceback

class GARClient:
    def __init__(self, endpoint: str, user: str, heartbeat_interval: int = 4000):
        """
        Initialize the GAR client.

        Args:
            endpoint: ZeroMQ endpoint (e.g., "tcp://localhost:5555")
            user: Client username
            heartbeat_interval: Heartbeat interval in milliseconds
        """
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.DEALER)

        hostname = socket.gethostname()
        pid = os.getpid()
        identity = f"{hostname}:{user}:{pid}".encode('utf-8')
        self.socket.setsockopt(zmq.IDENTITY, identity)
        self.logger = logging.getLogger(__name__)
        self.logger.debug(f"Set socket identity: {identity.decode('utf-8')}")

        self.socket.connect(endpoint)

        self.user = user
        self.heartbeat_interval = heartbeat_interval
        self.version = 650269

        self.server_topic_map: Dict[int, str] = {}
        self.server_key_map: Dict[int, str] = {}

        self.local_topic_counter = 1
        self.local_key_counter = 1
        self.local_topic_map: Dict[str, int] = {}
        self.local_key_map: Dict[str, int] = {}

        self.running = False
        self.heartbeat_thread = None

        self.message_handlers: Dict[str, Callable[[Dict[str, Any]], None]] = {}

        self.last_heartbeat_time = time.time()
        self.heartbeat_timeout = 30  # Default 30 seconds

        # Lock for synchronizing send operations
        self.send_lock = threading.Lock()

        # Record map: (key_id, topic_id) -> record value
        self.record_map: Dict[Tuple[int, int], Any] = {}

        logging.basicConfig(level=logging.INFO)
        self.register_default_handlers()

    def register_handler(self, message_type: str, handler: Callable[[Dict[str, Any]], None]):
        """Register a callback handler for a specific message type."""
        self.message_handlers[message_type] = handler

    def register_introduction_handler(self, handler: Callable[[int, int, str, Optional[str]], None]):
        """Handler for Introduction: (version, heartbeat_timeout_interval, user, schema)"""

        def wrapper(msg: Dict[str, Any]):
            value = msg["value"]
            handler(value["version"], value["heartbeat_timeout_interval"],
                    value["user"], value.get("schema"))

        self.register_handler("Introduction", wrapper)

    def register_heartbeat_handler(self, handler: Callable[[], None]):
        """Handler for Heartbeat: no arguments"""

        def wrapper(msg: Dict[str, Any]):
            handler()

        self.register_handler("Heartbeat", wrapper)

    def register_logoff_handler(self, handler: Callable[[], None]):
        """Handler for Logoff: no arguments"""

        def wrapper(msg: Dict[str, Any]):
            handler()

        self.register_handler("Logoff", wrapper)

    def register_topic_introduction_handler(self, handler: Callable[[int, str], None]):
        """Handler for TopicIntroduction: (topic_id, name)"""

        def wrapper(msg: Dict[str, Any]):
            value = msg["value"]
            handler(value["topic_id"], value["name"])

        self.register_handler("TopicIntroduction", wrapper)

    def register_key_introduction_handler(self, handler: Callable[[int, str, Optional[str]], None]):
        """Handler for KeyIntroduction: (key_id, name, _class)"""

        def wrapper(msg: Dict[str, Any]):
            value = msg["value"]
            handler(value["key_id"], value["name"], value.get("_class"))

        self.register_handler("KeyIntroduction", wrapper)

    def register_delete_key_handler(self, handler: Callable[[int], None]):
        """Handler for DeleteKey: (key_id)"""

        def wrapper(msg: Dict[str, Any]):
            handler(msg["value"]["key_id"])

        self.register_handler("DeleteKey", wrapper)

    def register_subscribe_handler(self, handler: Callable[[str, int, str, int, int, Optional[str], Optional[str], Optional[str]], None]):
        """Handler for Subscribe: (subscription_mode, nagle_interval, name, key_id, topic_id, _class, key_filter, topic_filter)"""

        def wrapper(msg: Dict[str, Any]):
            value = msg["value"]
            handler(value["subscription_mode"], value["nagle_interval"], value["name"],
                    value["key_id"], value["topic_id"], value.get("_class"),
                    value.get("key_filter"), value.get("topic_filter"))

        self.register_handler("Subscribe", wrapper)

    def register_snapshot_complete_handler(self, handler: Callable[[str], None]):
        """Handler for SnapshotComplete: (name)"""

        def wrapper(msg: Dict[str, Any]):
            handler(msg["value"]["name"])

        self.register_handler("SnapshotComplete", wrapper)

    def register_unsubscribe_handler(self, handler: Callable[[str], None]):
        """Handler for Unsubscribe: (name)"""

        def wrapper(msg: Dict[str, Any]):
            handler(msg["value"]["name"])

        self.register_handler("Unsubscribe", wrapper)

    def register_new_record_handler(self, handler: Callable[[int, int], None]):
        """Handler for NewRecord: (key_id, topic_id)"""

        def wrapper(msg: Dict[str, Any]):
            value = msg["value"]
            handler(value["key_id"], value["topic_id"])

        self.register_handler("NewRecord", wrapper)

    def register_delete_record_handler(self, handler: Callable[[int, int], None]):
        """Handler for DeleteRecord: (key_id, topic_id)"""

        def wrapper(msg: Dict[str, Any]):
            value = msg["value"]
            handler(value["key_id"], value["topic_id"])

        self.register_handler("DeleteRecord", wrapper)

    def register_record_update_handler(self, handler: Callable[[int, int, Any], None]):
        """Handler for JSONRecordUpdate: (key_id, topic_id, value)"""

        def wrapper(msg: Dict[str, Any]):
            record_id = msg["value"]["record_id"]
            handler(record_id["key_id"], record_id["topic_id"], msg["value"]["value"])

        self.register_handler("JSONRecordUpdate", wrapper)

    def register_shutdown_handler(self, handler: Callable[[], None]):
        """Handler for Shutdown: no arguments"""

        def wrapper(msg: Dict[str, Any]):
            handler()

        self.register_handler("Shutdown", wrapper)

    def register_default_handlers(self):
        """Register default logging handlers for all message types."""
        self.register_introduction_handler(
            lambda version, interval, user, schema: self.logger.info(f"Connected to server: {user}"))
        self.register_heartbeat_handler(
            lambda: self.logger.debug("Heartbeat received"))
        self.register_logoff_handler(
            lambda: self.logger.info("Logoff received"))
        self.register_topic_introduction_handler(
            lambda topic_id, name: self.logger.info(f"New server topic: {name} (Server ID: {topic_id})"))
        self.register_key_introduction_handler(
            lambda key_id, name, _class: self.logger.info(f"New server key: {name} (Server ID: {key_id})"))
        self.register_delete_key_handler(
            lambda key_id: self.logger.info(f"Delete key: {self.server_key_map.get(key_id)} (Server ID: {key_id})"))
        self.register_subscribe_handler(
            lambda mode, interval, name, key_id, topic_id, _class, key_filter, topic_filter:
            self.logger.info(f"Subscribe: {name} (mode: {mode})"))
        self.register_snapshot_complete_handler(
            lambda name: self.logger.info(f"Snapshot complete for subscription: {name}"))
        self.register_unsubscribe_handler(
            lambda name: self.logger.info(f"Unsubscribe: {name}"))
        self.register_new_record_handler(
            lambda key_id, topic_id: self.logger.info(
                f"New record: {self.server_key_map.get(key_id)} - {self.server_topic_map.get(topic_id)}"))
        self.register_delete_record_handler(
            lambda key_id, topic_id: self.logger.info(
                f"Delete record: {self.server_key_map.get(key_id)} - {self.server_topic_map.get(topic_id)}"))
        self.register_record_update_handler(
            lambda key_id, topic_id, value: self.logger.info(
                f"Record update: {self.server_key_map.get(key_id)} - {self.server_topic_map.get(topic_id)} = {value}"))
        self.register_shutdown_handler(
            lambda: self.logger.info("Shutdown received"))

    def start(self):
        """Start the client and send introduction message."""
        self.running = True
        intro_msg = {
            "message_type": "Introduction",
            "value": {
                "version": self.version,
                "heartbeat_timeout_interval": self.heartbeat_interval,
                "user": self.user
            }
        }
        self.send_message(intro_msg)
        self.heartbeat_thread = threading.Thread(target=self._heartbeat_loop, daemon=True)
        self.heartbeat_thread.start()
        self._receive_loop()

    def stop(self):
        """Stop the client and send logoff message."""
        self.send_message({"message_type": "Logoff"})
        self.running = False  # Signal the receive loop to stop
        if self.heartbeat_thread:
            self.heartbeat_thread.join()  # Wait for heartbeat thread to finish


    def __del__(self):
        """Clean up ZeroMQ resources when the object is destroyed."""
        if hasattr(self, 'socket') and self.socket:
            self.socket.close()
        if hasattr(self, 'context') and self.context:
            self.context.term()

    def send_message(self, message: Dict[str, Any]):
        """Send a JSON message through the socket using ZeroMQ DEALER protocol."""
        msg_str = json.dumps(message)
        with self.send_lock:
            self.socket.send_multipart([b'', msg_str.encode('utf-8')])
        self.logger.debug(f"Sent: {msg_str}")

    def _heartbeat_loop(self):
        """Send periodic heartbeat messages."""
        while self.running:
            self.send_message({"message_type": "Heartbeat"})
            time.sleep(self.heartbeat_interval / 1000 / 2)

    def _receive_loop(self):
        """Main receive loop for processing server messages."""
        poller = zmq.Poller()
        poller.register(self.socket, zmq.POLLIN)

        while self.running:
            # Check heartbeat timeout
            current_time = time.time()
            if current_time - self.last_heartbeat_time > self.heartbeat_timeout:
                self.logger.warning(f"No heartbeat received within {self.heartbeat_timeout} seconds, exiting")
                self.running = False
                break

            # Poll for messages with a 1-second timeout
            events = poller.poll(1000)  # 1000 ms = 1 second
            if events:
                try:
                    parts = self.socket.recv_multipart()
                    if len(parts) < 2:
                        self.logger.error(f"Received malformed message with {len(parts)} parts: {parts}")
                        continue
                    message_bytes = parts[1]
                    message = message_bytes.decode('utf-8')
                    msg = json.loads(message)
                    self._process_message(msg)
                except Exception as e:
                    self.logger.error(f"Error receiving message: {e}\n{traceback.format_exc()}")
                    break
            # No else clause needed; loop continues to check timeout

    def _process_message(self, message: Dict[str, Any]):
        """Process incoming messages by calling registered handlers."""
        msg_type = message.get("message_type")
        if msg_type == "TopicIntroduction":
            self.server_topic_map[message["value"]["topic_id"]] = message["value"]["name"]
        elif msg_type == "KeyIntroduction":
            self.server_key_map[message["value"]["key_id"]] = message["value"]["name"]
        elif msg_type == "Heartbeat":
            self.last_heartbeat_time = time.time()  # Update on heartbeat
        elif msg_type == "Introduction":
            value = message["value"]
            self.heartbeat_timeout = value["heartbeat_timeout_interval"] / 1000  # Convert ms to seconds
            self.last_heartbeat_time = time.time()  # Reset on introduction
        elif msg_type == "JSONRecordUpdate":
            record_id = message["value"]["record_id"]
            key_id = record_id["key_id"]
            topic_id = record_id["topic_id"]
            record_value = message["value"]["value"]
            self.record_map[(key_id, topic_id)] = record_value  # Store the record value
        elif msg_type == "DeleteRecord":
            value = message["value"]
            key_id = value["key_id"]
            topic_id = value["topic_id"]
            self.record_map.pop((key_id, topic_id), None)  # Remove the record if it exists
        elif msg_type == "Logoff":
            self.logger.info("Received Logoff from server, shutting down")
            self.running = False
            return

        handler = self.message_handlers.get(msg_type)
        if handler:
            handler(message)
        else:
            self.logger.warning(f"No handler registered for message type: {msg_type}")

    def subscribe(self, name: str, mode: str = "Streaming",
                  key_name: Optional[str] = None, topic_name: Optional[str] = None,
                  class_filter: Optional[str] = None, key_filter: Optional[str] = None,
                  topic_filter: Optional[str] = None):
        """Send a subscription request using local IDs."""
        key_id = self.get_and_possibly_introduce_key_id(key_name) if key_name else 0
        topic_id = self.get_and_possibly_introduce_topic_id(topic_name) if topic_name else 0
        sub_msg = {
            "message_type": "Subscribe",
            "value": {
                "subscription_mode": mode,
                "nagle_interval": 0,
                "name": name,
                "key_id": key_id,
                "topic_id": topic_id,
                "_class": class_filter,
                "key_filter": key_filter,
                "topic_filter": topic_filter
            }
        }
        self.send_message(sub_msg)

    def get_and_possibly_introduce_key_id(self, name: str, class_name: Optional[str] = None) -> int:
        """Introduce a new key if not already known and return local key ID."""
        if name not in self.local_key_map:
            key_id = self.local_key_counter
            self.local_key_map[name] = key_id
            self.local_key_counter += 1
            msg = {
                "message_type": "KeyIntroduction",
                "value": {
                    "key_id": key_id,
                    "name": name,
                    "_class": class_name
                }
            }
            self.send_message(msg)
        return self.local_key_map[name]

    def get_and_possibly_introduce_topic_id(self, name: str) -> int:
        """Introduce a new topic if not already known and return local topic ID."""
        if name not in self.local_topic_map:
            topic_id = self.local_topic_counter
            self.local_topic_map[name] = topic_id
            self.local_topic_counter += 1
            msg = {
                "message_type": "TopicIntroduction",
                "value": {
                    "topic_id": topic_id,
                    "name": name
                }
            }
            self.send_message(msg)
        return self.local_topic_map[name]

    def publish_delete_key(self, key_id: int):
        """Publish a DeleteKey message using a local key ID."""
        msg = {
            "message_type": "DeleteKey",
            "value": {
                "key_id": key_id
            }
        }
        self.send_message(msg)

    def publish_delete_record(self, key_id: int, topic_id: int):
        """Publish a DeleteRecord message using local key and topic IDs."""
        msg = {
            "message_type": "DeleteRecord",
            "value": {
                "key_id": key_id,
                "topic_id": topic_id
            }
        }
        self.send_message(msg)

    def publish_unsubscribe(self, name: str):
        """Publish an Unsubscribe message for a subscription name."""
        msg = {
            "message_type": "Unsubscribe",
            "value": {
                "name": name
            }
        }
        self.send_message(msg)

    def publish_shutdown(self):
        """Publish a Shutdown message."""
        msg = {
            "message_type": "Shutdown"
        }
        self.send_message(msg)

    def publish_record_with_ids(self, key_id: int, topic_id: int, value: Any):
        """Publish a record update using pre-looked-up local IDs."""
        new_record_msg = {
            "message_type": "NewRecord",
            "value": {
                "key_id": key_id,
                "topic_id": topic_id
            }
        }
        self.send_message(new_record_msg)
        update_msg = {
            "message_type": "JSONRecordUpdate",
            "value": {
                "record_id": {
                    "key_id": key_id,
                    "topic_id": topic_id
                },
                "value": value
            }
        }
        self.send_message(update_msg)

    def publish_record(self, key_name: str, topic_name: str, value: Any):
        """Publish a record update using names, converting to local IDs."""
        key_id = self.get_and_possibly_introduce_key_id(key_name)
        topic_id = self.get_and_possibly_introduce_topic_id(topic_name)
        self.publish_record_with_ids(key_id, topic_id, value)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GAR Protocol Client")
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="ZeroMQ IP address (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=5555,
                        help="ZeroMQ port (default: 5555)")
    parser.add_argument("--user", type=str, default=None,
                        help="Username (default: OS environment username)")
    parser.add_argument("--log-level", type=str, default="INFO",
                        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                        help="Logging level (default: INFO)")
    # Subscription arguments
    parser.add_argument("--streaming", action="store_true",
                        help="Stay running and stream updates. Otherwise exit after snapshot received.")
    parser.add_argument("--key-filter", type=str, default=None,
                        help="Key filter regex pattern")
    parser.add_argument("--class", type=str, default=None,
                        help="Class name")
    parser.add_argument("--topic-filter", type=str, default=None,
                        help="Topic filter regex pattern")
    parser.add_argument("--send-shutdown", action="store_true",
                        help="Shut down the server")

    args = parser.parse_args()
    username = args.user if args.user is not None else getpass.getuser()
    endpoint = f"tcp://{args.ip}:{args.port}"

    # Configure logging based on argument
    log_level = getattr(logging, args.log_level.upper())
    logging.basicConfig(level=log_level)

    client = GARClient(endpoint, username)


    def custom_topic_handler(topic_id: int, name: str):
        print(f"Custom topic: {name} (ID: {topic_id})")


    def custom_record_update_handler(key_id: int, topic_id: int, value: Any):
        key_name = client.server_key_map.get(key_id, "Unknown")
        topic_name = client.server_topic_map.get(topic_id, "Unknown")
        print(f"Custom update: {key_name} {topic_name} = {value}")


    def custom_delete_key_handler(key_id: int):
        key_name = client.server_key_map.get(key_id, "Unknown")
        print(f"Custom delete key: {key_name} (ID: {key_id})")


    client.register_topic_introduction_handler(custom_topic_handler)
    client.register_record_update_handler(custom_record_update_handler)
    client.register_delete_key_handler(custom_delete_key_handler)

    try:
        client_thread = threading.Thread(target=client.start)
        client_thread.start()

        #Need to release the GIL for the client thread to send introduction
        time.sleep(1)

        if args.send_shutdown:
            client.publish_shutdown()
            client.stop()
        else:
            subscription_mode = "Streaming" if args.streaming else "Snapshot"
            client.subscribe("S1", mode=subscription_mode,
                             key_name=None, topic_name=None,
                             class_filter=args.__dict__["class"],
                             key_filter=args.key_filter,
                             topic_filter=args.topic_filter)

            # time.sleep(1)
            #
            # client.publish_record("IBM", "baseline_volatility", .25)
            #
            # aapl_id = client.get_and_possibly_introduce_key_id("AAPL")
            # baseline_volatility_id = client.get_and_possibly_introduce_topic_id("baseline_volatility")
            # client.publish_record_with_ids(aapl_id, baseline_volatility_id, .38)

            # client.publish_unsubscribe("S1")

            # client.publish_delete_key(client.get_and_possibly_introduce_key_id("MSFT"))
            # client.publish_delete_record(client.get_and_possibly_introduce_key_id("tst"), baseline_volatility_id)

            if subscription_mode == "Snapshot":
                client.stop()

        client_thread.join()

    except KeyboardInterrupt:
        client.stop()
