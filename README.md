# Парсер книг с сайта tululu.org

Скрипт позволяет скачивать книги с сайта [tululu.org](https://tululu.org/) в формате .txt с обложками и комментариями.

### Как установить

1. Предварительно должен быть установлен Python3.
2. Для установки зависимостей:
```
pip install -r requirements.txt
```
3. Для запуска скрипта:
```
$ python main.py
```

### Аргументы
Скрипт может принимать следующие аргументы:
`--start_page`: с какой книги начинать скачивание
`--end_page`: по какую книгу скачивать

Например данная команда скачает книги от 20 по 30:
```
$ python main.py 20 30
```