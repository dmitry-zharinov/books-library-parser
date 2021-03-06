import logging
import os
import time
from parser import parse_book_page
from pathlib import Path
from urllib.parse import urlsplit

import requests
from pathvalidate import sanitize_filename

logger = logging.getLogger(__file__)


HOST_NAME = 'https://tululu.org'
BOOKS_FOLDER = 'books'
IMG_FOLDER = 'images'


def check_for_redirect(response: requests.Response):
    if response.history:
        raise requests.exceptions.HTTPError('Книга не найдена')


def download_txt(url: str, payload: dict, filename: str, folder: Path):
    """Функция для скачивания текстовых файлов"""
    folder.mkdir(parents=True, exist_ok=True)

    response = requests.get(url, payload)
    response.raise_for_status()
    check_for_redirect(response)

    filepath = os.path.join(folder, f'{sanitize_filename(filename)}.txt')
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(response.text)

    return filepath


def download_image(url: str, folder: Path):
    """Функция для скачивания обложек"""
    folder.mkdir(parents=True, exist_ok=True)
    filename = urlsplit(url).path.split('/')[-1]
    response = requests.get(url)
    response.raise_for_status()

    with open(folder / filename, 'wb') as file:
        file.write(response.content)


def download_book_with_image(book_id: str,
                             dest_folder: Path,
                             skip_imgs: bool,
                             skip_txt: bool):
    """Скачать книгу с обложкой"""
    payload = {
        'id': book_id,
    }
    try:
        book_url = f'https://tululu.org/b{book_id}/'
        response = requests.get(book_url)
        response.raise_for_status()
        check_for_redirect(response)
        book_metadata = parse_book_page(response.text, book_url)

        if not skip_txt:
            download_txt(
                'https://tululu.org/txt.php',
                payload,
                f'{book_metadata["title"]}',
                dest_folder / BOOKS_FOLDER)

        if not skip_imgs:
            download_image(
                    book_metadata['img_src'],
                    dest_folder / IMG_FOLDER)

        return book_metadata

    except requests.exceptions.HTTPError as http_err:
        logging.error(http_err)
    except requests.ConnectionError as e:
        logging.error(e)
        time.sleep(10)
