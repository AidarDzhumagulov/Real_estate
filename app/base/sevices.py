from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.utils.queue_connector import KafkaConnector


class KafkaService:
    def __init__(self, connector: "KafkaConnector"):
        self.connector = connector

    async def send_message(self, message: dict, topic_name: str) -> None:
        """
        Sends a message to the specified Kafka topic.

        :param message: Dictionary containing the message payload to be sent.
        :param topic_name: Name of the Kafka topic where the message should be sent.
        :return: None.
        """
        await self.connector.send_message(message=message, topic_name=topic_name)
