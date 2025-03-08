from confluent_kafka.error import KafkaError, KafkaException

from src.configs import config, poetry_config, LOGGER
from src.connections import MainKafkaConnector, KafkaConnector
from src.models.meta import MessageDTO


class BaseEngine:
    def __init__(self):
        self.config = config
        self.project_config = poetry_config
        self.status_running = True

    def run(self, broker: MainKafkaConnector | KafkaConnector):
        LOGGER.info("Application started.")
        LOGGER.info("Press Ctrl + C to stop ...")

        try:
            broker.initizalize_consumer()
            broker.consumer.subscribe([self.config.kafka.topics])

            while self.status_running:
                if messages := broker.consumer.consume(1, 1.0):
                    for message in messages:

                        if message.error():
                            if message.error().code() == KafkaError._PARTITION_EO:
                                LOGGER.warning(
                                    f"{message.topic()} [{message.partition()}] reached end at offset {message.offset()}"
                                )
                            else:
                                raise KafkaException(message.error())

                        payload = MessageDTO.model_validate_json(message.value())

                        # ? Handling payload here
                        LOGGER.info(f"Message: {payload}")
        except KeyboardInterrupt:
            LOGGER.warning("Application stopped forcely.")
            raise
        except Exception as e:
            LOGGER.exception(e)
        finally:
            broker.close()


def runner():
    engine = BaseEngine()
    # engine.run(broker=KafkaConnector(config.kafka))
    engine.run(broker=MainKafkaConnector())


if __name__ == "__main__":

    engine = BaseEngine()
    engine.run(broker=MainKafkaConnector())
