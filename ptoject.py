import os
import csv
from glob import glob

from tabulate import tabulate


class PriceMachine:

    def __init__(self):
        self.data = []
        self.result = ''

    def load_prices(self, file_path=''):
        paths = glob('price*.csv')

        for file in paths:
            with open(os.path.join(file_path, file), encoding='utf-8') as f:
                reader = csv.DictReader(f, delimiter=',')

                for (
                    name, price,
                    weight, price_per_kg
                ) in self._search_product_price_weight(
                    reader
                ):
                    self.data.append(
                        {
                            'name': name,
                            'price': price,
                            'weight': weight,
                            'price_per_kg': price_per_kg,
                            'file': file
                        }
                    )
        self.data.sort(key=lambda x: x['price_per_kg'])

    @staticmethod
    def _search_product_price_weight(reader):
        name_col = ''
        price_col = ''
        weight_col = ''
        for col in reader.fieldnames:
            if col in ['товар', 'название', 'наименование', 'продукт']:
                name_col = col
            if col in ['розница', 'цена']:
                price_col = col
            if col in ['вес', 'масса', 'фасовка']:
                weight_col = col
        if not all((name_col, price_col, weight_col)):
            raise ValueError('Не найдены необходимые колонки')
        for row in reader:
            name = row[name_col]

            price = float(row[price_col].replace(',', '.'))
            weight = float(row[weight_col].replace(',', '.'))
            price_per_kg = price / weight
            yield name, price, weight, price_per_kg

    def find_text(self, text):
        filtered_data = [
            item for item in self.data if text.lower() in item['name'].lower()
        ]
        print(tabulate(filtered_data, headers='keys'))
        return filtered_data

    def export_to_html(self, filename='output.html'):
        self.result = '<html><meta charset="utf-8"><body>'

        self.result += tabulate(self.data, headers='keys', tablefmt='html')

        self.result += '</body></html>'

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(self.result)


if __name__ == '__main__':
    path = './'
    pm = PriceMachine()
    pm.load_prices(path)
    print("Для поска товара напишите его название. Если поиск окончен напишите 'exit'.")
    while True:
        input_text = input('Введите текст для поиска: ')
        if input_text != 'exit':
            pm.find_text(input_text)
        else:
            pm.export_to_html()
            print('Спасибо за работу!')
            print('The end')
            break
