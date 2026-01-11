import psycopg2
import uuid


class DBWriter:
    def __init__(self,
                 host="localhost",
                 port=5432,
                 database="tg_mpl",
                 user="dan",
                 password="dan"):
        self.conn = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )

    def send_tag(self, photo_id: uuid.UUID, tag_value: str):
        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO tag (photo_id, tag)
                VALUES (%s, %s)
                """,
                (photo_id, tag_value)
            )
        self.conn.commit()

    def close(self):
        self.conn.close()
