import pickle
from logging import getLogger

from confluent_kafka import DeserializingConsumer, KafkaError, KafkaException

from mas.utils.config import Config
from mas.websocket.script.dto.script_response import ScriptResponse

logger = getLogger()


class ScriptConsumingService:
    def __init__(self, config: Config):
        self.kafka_config = config.kafka["consumer"]
        self.kafka_config["value.deserializer"] = lambda v: pickle.loads(v)

        self.consumer = DeserializingConsumer(self.kafka_config)

    def consume_script(
        self, meeting_id: int, user_id: int, script_response: ScriptResponse
    ):
        running = True

        try:
            self.consumer.subscribe("script")

            while running:
                msg = self.consumer.poll(timeout=1.0)
                if msg is None:
                    continue

                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        # End of partition event
                        logger.error(
                            f"{msg.topic()} [{msg.partition()} reached end at offset {msg.offset()}"
                        )
                    elif msg.error():
                        raise KafkaException(msg.error())
                else:
                    # msg_process(msg)
                    self.consumer.commit(asynchronous=True)
        finally:
            # Close down consumer to commit final offsets.
            self.consumer.close()
