import asyncio
from logging import getLogger

import inject

from mas.messaging.service.script_consuming_service import ScriptConsumingService

logger = getLogger()


def commit_completed(err, partitions):
    if err:
        print(str(err))
    else:
        print("Committed partition offsets: " + str(partitions))


conf = {
    "bootstrap.servers": "host1:9092,host2:9092",
    "group.id": "foo",
    "auto.offset.reset": "earliest",
    "on_commit": commit_completed,
}

script_consuming_service = inject.instance(ScriptConsumingService)

if __name__ == "__main__":
    asyncio.run(script_consuming_service.consume_script())
