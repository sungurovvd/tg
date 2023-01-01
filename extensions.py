import json
import requests
from config import keys


class APIException(Exception):
    pass


class Converter:
    @staticmethod
    def convert(base, quote, amount):
        try:
            base = keys.get(base.lower())
        except KeyError:
            raise APIException(f'Введена неправильная валюта: {base}')

        try:
            quote = keys.get(quote.lower())
        except KeyError:
            raise APIException(f'Введена неправильная валюта: {quote}')

        if base.lower() == quote.lower():
            raise APIException('Одинаковые валюты')

        try:
            amount = float(amount)
            if amount <= 0:
                raise APIException('Количество меньше или равно нулю')
        except ValueError:
            raise APIException(f'Не удалось обработать число: {amount}')

        base_rates = float(Converter.rates(base))
        quote_rates = float(Converter.rates(quote))
        return base, quote, quote_rates/base_rates*amount

    @staticmethod
    def rates(nmbr):
        url = f"https://openexchangerates.org/api/latest.json?app_id=41fb0493bb88440185e6973a5e5bd29c&base=USD&symbols={nmbr}&prettyprint=false&show_alternative=false"
        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers)
        answer = json.loads(response.content)
        print(response)
        return answer['rates'][f'{nmbr}']
