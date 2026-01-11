from kafka_consumer import MLPhotoConsumer
from object_detection import ObjectDetector
from utils import download_photo
from db_writer import DBWriter

if __name__ == '__main__':
    BROKER = 'localhost:9092'
    TOPIC = 'raw_photo_topic'
    GROUP = 'ml-processor-group-1'

    consumer_service = MLPhotoConsumer(BROKER, TOPIC, GROUP)

    object_detector = ObjectDetector()

    db_writer = DBWriter()

    try:
        while True:

            data = consumer_service.poll_message(timeout=1.0)

            if data:
                try:
                    photo_url = data.get('file_url')
                    photo_id = data.get('id')
                except Exception as e:
                    print(e)
                    continue
                if photo_url is None:
                    continue
                print(f"Получено сообщение: URL={photo_url}, Offset={data['__kafka_msg'].offset()}")

                photo_path = download_photo(photo_url)
                if photo_path is None:
                    print("Ошибка при сохранении фотографии")
                    continue

                objects = object_detector.detect_objects(photo_path)
                for tag in objects:
                    db_writer.send_tag(photo_id, tag)
                consumer_service.commit_offset(data['__kafka_msg'])

    except KeyboardInterrupt:
        db_writer.close()
        print("Прерывание пользователем.")
    finally:
        db_writer.close()
        consumer_service.close()
        print("Приложение завершено.")


