import pickle

from confluent_kafka import SerializingProducer

from mas.api.script.entity.script import Script
from mas.utils.config import Config
from mas.utils.kafka_utils import on_delivery
from mas.websocket.script.dto.script_response import ScriptResponse


class ScriptProducingService:
    def __init__(self, config: Config):
        self.kafka_config = config.kafka["producer"]
        self.kafka_config["value.serializer"] = lambda v: pickle.dumps(
            v, protocol=pickle.HIGHEST_PROTOCOL
        )

        self.producer = SerializingProducer(self.kafka_config)

    def consume_script(
        self, meeting_id: int, user_id: int, script_response: ScriptResponse
    ):
        script = Script(mid=meeting_id, uid=user_id, content=script_response.content)
        self.producer.produce("scripts", script, on_delivery=on_delivery)
