import json

from confluent_kafka import Producer

from mas.api.script.entity.script import Script
from mas.utils.config import Config
from mas.utils.kafka_utils import acked
from mas.websocket.script.dto.script_response import ScriptResponse


class ScriptProducingService:
    def __init__(self, config: Config):
        self.producer = Producer(config.kafka["producer"])

    def consume_script(
        self, meeting_id: int, user_id: int, script_response: ScriptResponse
    ):
        script = Script(mid=meeting_id, uid=user_id, content=script_response.content)
        self.producer.produce(
            "scripts", json.dumps(script).encode("utf-8"), callback=acked
        )
