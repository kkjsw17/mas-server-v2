import pickle
from logging import getLogger

from confluent_kafka import DeserializingConsumer, KafkaError, KafkaException
from messaging.repository.script_repository import ScriptRepository
from messaging.utils.config import Config

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

    def __init__(self, config: Config, script_repository: ScriptRepository):
        self.kafka_config = config.kafka["consumer"]
        self.kafka_config["value.deserializer"] = lambda v, ctx: pickle.loads(v)
        self.kafka_config["on_commit"] = commit_completed

        self.script_repository = script_repository

    async def consume_script(self):
        """
        Consume script from Kafka topic and save it in script repository.
        """

        consumer = DeserializingConsumer(self.kafka_config)
        running = True

        try:
            consumer.subscribe(["scripts"])

            while running:
                msg = consumer.poll(timeout=1.0)
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
                    print(msg.value())
                    # await self.script_repository.save(script=msg.value())
                    consumer.commit(asynchronous=True)
        finally:
            # Close down consumer to commit final offsets.
            consumer.close()
