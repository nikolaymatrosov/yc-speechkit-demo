import os

import requests

API_KEY = os.environ["API_KEY"]


def format_filename(i: int) -> str:
    return f"{i:05d}.ogg"


def make_req(text, n: int):
    # Сформируем заголовок запроса с ключем авторизации
    headers = {
        "Authorization": f"Api-Key {API_KEY}"
    }

    # Отправим запрос
    res = requests.post(
        "https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize",
        {
            "text": text,
            "lang": "ru-RU",
            "voice": "filipp",
            "emotion": "neutral"
        },
        headers=headers)

    # И запишем результат в файл
    filename = format_filename(n)
    with open(f"out/{filename}", "wb") as out:
        out.write(res.content)


def main(f_name):
    # Создадим директорию куда будем складывать результат
    try:
        os.mkdir("out")
    except:
        pass

    with open(f_name) as f:
        n = 1
        while line := f.readline():
            # Пропустим пустые строки
            if line == '\n':
                continue
            # Делим строку на предожения
            sentences = line.split('.')
            for sentence in sentences:
                # Убираем лишние пробелы и переводы строк
                sentence = sentence.strip(" \n")
                # И опять, пустые предложения пропускаем
                if not sentence:
                    continue
                # Возвращаем на место точки
                sentence = sentence + "."
                # Печатаем предложени
                print(n, sentence)
                # Делаем запрос
                make_req(sentence, n)
                n = n + 1

    # Собираем список созданных файлов
    with open("out/list.txt", "w") as f:
        for i in range(1, n + 1):
            filename = format_filename(i)
            line = f"file '{filename}'\n"
            f.write(line)

    # При помощи ffmpeg склеим все файлы в один
    os.system("ffmpeg -f concat -i out/list.txt -c copy out/output.ogg")


if __name__ == '__main__':
    main('book.txt')
