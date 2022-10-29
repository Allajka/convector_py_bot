from datetime import datetime as dt


def info_logger(data):
    time = dt.now().strftime('%d.%m.%Y - %H:%M:%S')
    with open('Log.txt', 'a', encoding="utf-8") as file:
        file.write(f'{time}: {data}\n')