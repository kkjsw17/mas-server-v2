import pickle

from confluent_kafka import DeserializingConsumer

from mas.utils.config import Config
from mas.websocket.script.dto.script_response import ScriptResponse


class ScriptConsumingService:
    def __init__(self, config: Config):
        self.kafka_config = config.kafka["consumer"]
        self.kafka_config["value.deserializer"] = lambda v: pickle.loads(v)

        self.consumer = DeserializingConsumer(self.kafka_config)

    def consume_script(
        self, meeting_id: int, user_id: int, script_response: ScriptResponse
    ):
        pass
        # script = Script(mid=meeting_id, uid=user_id, content=script_response.content)
        # self.consumer.poll(0)
