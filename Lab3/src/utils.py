from requests import get
import uuid


async def download_photo(photo_path="https://api.telegram.org/file/bot7568061137:AAE-dGd-FCKp5epiyZ6juv5PExjxrteEuVU/photos/file_1.jpg") -> str | None:
    filename = f"{uuid.uuid4()}.jpg"
    file_path = f"downloads/{filename}"
    response = get(photo_path, timeout=10)

    if response.status_code == 200:
        with open(file_path, "wb") as f:
            f.write(response.content)
        print("Фото успешно скачано")
        return file_path
    else:
        print("Ошибка при скачивании:", response.status_code)
        return None
