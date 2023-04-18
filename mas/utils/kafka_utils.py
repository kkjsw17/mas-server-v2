from logging import getLogger

logger = getLogger()


def on_delivery(err, msg):
    if err is not None:
        logger.error(f"Failed to deliver message: {str(msg)}: {str(err)}")
    else:
        logger.info(f"Message produced: {str(msg)}")


def delivery_report(err, msg):
    if err is not None:
        logger.error(f"Failed to deliver message: {str(err)}")
    else:
        logger.info(f"Message delivered to {str(msg.topic())} [{msg.partition()}]")
