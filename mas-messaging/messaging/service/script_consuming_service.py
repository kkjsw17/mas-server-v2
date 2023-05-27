import pickle
from logging import getLogger

import inject
from confluent_kafka import DeserializingConsumer, KafkaError, KafkaException

from mas.api.script.repository.script_repository import ScriptRepository
from mas.utils.config import Config

logger = getLogger()


def commit_completed(err, partitions):
    if err:
        logger.error(str(err))
    else:
        logger.info("Committed partition offsets: " + str(partitions))


class ScriptConsumingService:
    """
    Consumes scripts from a Kafka topic and saves them in a script repository.

    Args:
        config (Config): The configuration object containing the Kafka consumer configuration.

    Attributes:
        kafka_config (dict): The configuration options for the Kafka consumer, including the value deserializer and the on-commit function.
        consumer (DeserializingConsumer): The Kafka consumer instance.
    """

    def __init__(self, config: Config):
        self.kafka_config = config.kafka["consumer"]
        self.kafka_config["value.deserializer"] = lambda v: pickle.loads(v)
        self.kafka_config["on_commit"] = commit_completed

        self.consumer = DeserializingConsumer(self.kafka_config)

    @inject.params(script_repository=ScriptRepository)
    async def consume_script(self, script_repository: ScriptRepository):
        """
        Consume script from Kafka topic and save it in script repository.

        Args:
            script_repository (ScriptRepository): An instance of the ScriptRepository class containing the methods to save the script.
        """

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
                    await script_repository.save(msg)
        finally:
            # Close down consumer to commit final offsets.
            self.consumer.close()
