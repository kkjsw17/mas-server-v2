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


script_consuming_service = inject.instance(ScriptConsumingService)

if __name__ == "__main__":
    asyncio.run(script_consuming_service.consume_script())
