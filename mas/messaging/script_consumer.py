from logging import getLogger

from confluent_kafka import Consumer, KafkaError, KafkaException

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

consumer = Consumer(conf)


running = True


def consume_loop(consumer, topics):
    try:
        consumer.subscribe(topics)

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
                consumer.commit(asynchronous=True)
    finally:
        # Close down consumer to commit final offsets.
        consumer.close()
