import pickle
from logging import getLogger

import inject
from confluent_kafka import DeserializingConsumer, KafkaError, KafkaException

from mas.api.script.repository.script_repository import ScriptRepository
from mas.utils.config import Config

logger = getLogger()


def commit_completed(err, partitions):
    if err:
        print(str(err))
    else:
        print("Committed partition offsets: " + str(partitions))


class ScriptConsumingService:
    def __init__(self, config: Config):
        self.kafka_config = config.kafka["consumer"]
        self.kafka_config["value.deserializer"] = lambda v: pickle.loads(v)
        self.kafka_config["on_commit"] = commit_completed

        self.consumer = DeserializingConsumer(self.kafka_config)

    @inject.params(script_repository=ScriptRepository)
    async def consume_script(self, script_repository: ScriptRepository):
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
