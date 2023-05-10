import asyncio

import inject

from mas.messaging.service.script_consuming_service import ScriptConsumingService

script_consuming_service = inject.instance(ScriptConsumingService)

if __name__ == "__main__":
    asyncio.run(script_consuming_service.consume_script())
