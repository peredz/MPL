from confluent_kafka import Consumer, KafkaException, KafkaError
import json
import sys
from typing import Tuple, Optional


class MLPhotoConsumer:
    """
    Класс консюмера для Kafka, настроенный на ручное подтверждение (commit).
    """

    def __init__(self, broker_address: str, topic_name: str, group_id: str):
        self.topic = topic_name
        self.config = {
            'bootstrap.servers': broker_address,
            'group.id': group_id,
            'auto.offset.reset': 'earliest',
            'enable.auto.commit': False,
        }

        try:
            self.consumer = Consumer(self.config)
            print(f"Consumer успешно создан для группы: {group_id}")
        except KafkaException as e:
            print(f"Ошибка при создании Consumer: {e}")
            sys.exit(1)

        self.consumer.subscribe([self.topic])
        print(f"Подписан на топик: {self.topic}")

    def poll_message(self, timeout=1.0) -> Tuple[Optional[dict], Optional[Consumer]]:
        """
        Слушает Kafka и возвращает данные сообщения и объект Kafka.
        """
        msg = self.consumer.poll(timeout=timeout)

        if msg is None:
            return None, None

        if msg.error():
            if msg.error().code() == KafkaError.PARTITION_EOF:
                return None, None
            elif msg.error():
                print(f"Ошибка Consumer: {msg.error()}")
                return None, None

        # Успешно получено сообщение
        try:
            message_data = json.loads(msg.value().decode('utf-8'))

            return message_data, msg

        except Exception as e:
            print(f"Непредвиденная ошибка при обработке сообщения: {e}")
            # В случае ошибки декодирования или парсинга
            return None, None

    def commit_offset(self, msg) -> bool:
        """
        Подтверждает офсет сообщения после его успешной обработки.
        """
        try:
            # Используем msg для явного подтверждения офсета
            self.consumer.commit(message=msg, asynchronous=False)
            return True
        except KafkaException as e:
            print(f"ОШИБКА COMMIT: Не удалось подтвердить офсет: {e}")
            return False

    def close(self):
        print("Закрытие Consumer...")
        self.consumer.close()