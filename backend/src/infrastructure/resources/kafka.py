from faststream.kafka import KafkaBroker

from config import KafkaConfig


def new_kafka_broker(kafka_config: KafkaConfig) -> KafkaBroker:
    return KafkaBroker(kafka_config.server)
