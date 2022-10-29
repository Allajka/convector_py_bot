import requests
import json
from logger import *

def button_click(from_what_currency, amount, in_what_currency, username):
    url = f"https://api.apilayer.com/fixer/convert?to={in_what_currency}&from={from_what_currency}&amount={amount}"

    payload = {}
    headers = {
        "apikey": "5R4rxwCfb1pNf3yFFBDMuWgufpMORVji"  # токен
    }

    response = requests.request("GET", url, headers=headers, data=payload)  # запрос
    result = json.loads(response.text)
    status_code = result['success']

    if status_code:
        answer = f"{result['query']['amount']} {result['query']['from']} = {round(int(result['result']),3)} {result['query']['to']}"
        info_logger(f"{username} - Запрос обработан: {answer}")
        return answer
    else:
        info_logger(f"{username} - Запрос не обработан: from = {from_what_currency}, amount = {amount}, to = {in_what_currency}")
        return("❗ ❗ ❗ \nНе верный ввод валюты. Необходимо указать трехбуквенный международный код валюты.")
