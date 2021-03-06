import argparse
import json
import logging
from pathlib import Path

from download_books import download_book_with_image
from parser import get_book_ids

logger = logging.getLogger(__file__)


MEDIA_FOLDER = 'media'

def createParser():
    """Создание парсера аргументов"""
    parser = argparse.ArgumentParser(
        description='Скачивание книг жанра научной фантастики')

    parser.add_argument(
        '--start_page',
        help='С какого номера страницы начинать скачивание (по умолчанию - 1)',
        type=int,
        default=1)

    parser.add_argument(
        '--end_page',
        help='По какую страницу скачивать (по умолчанию - 10)',
        type=int,
        default=10)

    parser.add_argument(
        '--dest_folder',
        help='Путь к каталогу с результатами парсинга: '
             'картинкам, книгам (по умолчанию - каталог скрипта)',
        type=Path,
        default=Path.cwd() / MEDIA_FOLDER)

    parser.add_argument(
        '--skip_imgs',
        help='Не скачивать картинки',
        action='store_true')

    parser.add_argument(
        '--skip_txt',
        help='Не скачивать .txt-файлы',
        action='store_true')

    parser.add_argument(
        '--json_path',
        help='Путь к каталогу с *.json файлом с результатами'
             'работы скрипта (по умолчанию - каталог скрипта)',
        type=Path,
        default=Path.cwd() / MEDIA_FOLDER)
    return parser


def main():
    logging.basicConfig(level=logging.ERROR)
    logger.setLevel(logging.DEBUG)

    parser = createParser()
    params = parser.parse_args()

    sci_fi_url = 'https://tululu.org/l55/'
    book_ids = get_book_ids(
        sci_fi_url,
        params.start_page,
        params.end_page)

    downloaded_books = []
    for book_id in book_ids:
        book_metadata = download_book_with_image(
            book_id=book_id,
            dest_folder=params.dest_folder,
            skip_imgs=params.skip_imgs,
            skip_txt=params.skip_txt)
        if book_metadata:
            downloaded_books.append(book_metadata)

    json_path = params.json_path / "books.json"
    with open(json_path, "w", encoding="utf-8") as books_serialized:
        json.dump(
            downloaded_books,
            books_serialized,
            indent=4,
            ensure_ascii=False)


if __name__ == '__main__':
    main()
