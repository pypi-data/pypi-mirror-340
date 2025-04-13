import os
import requests

def download_file(url, filename):
    """Скачивает файл по URL и сохраняет его в папке пакета."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        # Получаем путь к директории пакета
        package_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(package_dir, filename)
        
        with open(file_path, 'wb') as f:
            f.write(response.content)
        print(f"Файл {filename} успешно скачан в {package_dir}")
    except Exception as e:
        print(f"Ошибка при скачивании файла: {e}")

# URL файла для скачивания (можно заменить на любой другой .txt файл)
FILE_URL = "https://example.com/sample.txt"  # Замените на реальный URL
FILE_NAME = "downloaded_file.txt"

# Скачиваем файл при импорте библиотеки
download_file(FILE_URL, FILE_NAME)