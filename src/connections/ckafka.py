from confluent_kafka import Consumer, Producer

from src.configs import config, LOGGER, CustomLogLevel
from src.models.connection import KafkaMeta


class KafkaConnector:

    consumer: Consumer
    producer: Producer

    def __init__(self, meta: KafkaMeta) -> None:
        self._meta: KafkaMeta = meta

    def initizalize_producer(self) -> None:
        try:
            self.producer = Producer(self._meta.confluent_config())
            LOGGER.log(CustomLogLevel.CONNECTION, "Kafka connected.")
        except Exception as e:
            raise e

    def initizalize_consumer(self) -> None:
        try:
            self.consumer = Consumer(self._meta.confluent_config())
            LOGGER.log(CustomLogLevel.CONNECTION, "Kafka connected.")
        except Exception as e:
            raise e

    def close(self) -> None:
        if hasattr(self, "consumer") and self.consumer:
            self.consumer.close()
        LOGGER.log(CustomLogLevel.CONNECTION, "Kafka disconnected.")


class MainKafkaConnector(KafkaConnector):
    def __init__(self) -> None:
        super().__init__(meta=config.kafka)
