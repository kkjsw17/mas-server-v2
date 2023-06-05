import pickle

from chat.script.dto.script_dto import ScriptDto
from chat.script.entity.script import Script
from chat.utils.config import Config
from chat.utils.kafka_utils import on_delivery
from confluent_kafka import SerializingProducer


class ScriptProducingService:
    def __init__(self, config: Config):
        self.kafka_config = config.kafka["producer"]
        self.kafka_config["value.serializer"] = lambda v, ctx: pickle.dumps(
            v, protocol=pickle.HIGHEST_PROTOCOL
        )

    def produce_script(self, meeting_id: int, user_id: int, script_dto: ScriptDto):
        script = Script(mid=meeting_id, uid=user_id, content=script_dto.content)

        producer = SerializingProducer(self.kafka_config)
        producer.produce(topic="testtest", value=script, on_delivery=on_delivery)
        producer.poll(1)
