# https://pro.coinmarketcap.com/account
# [-1] - отсечь справа одну цифру
import os
import json
import time
from datetime import datetime
from functools import wraps
from typing import Optional, Union

from coinmarketcapapi import CoinMarketCapAPI
from secret import secret
from .helpers.constants import *
from logger import log
from notify import Telega
from notify.modules.interfaces.isender import ISender
from prettytable import PrettyTable



def api_except(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            instance = args[0]
            current_key = instance._current_apikey
            log.error(f'{current_key} is limit ?, {e}')
            return None

    return inner


class MarketCapMonitor:
    def __init__(self, notification: ISender):
        self.apikeys = secret.coinmarketcap.apikeys
        self.data = self._load_db()
        self.notify = notification
        self.api = self._api_generator()
        self._current_apikey: Optional[str] = None

    def _api_generator(self):
        while True:
            for apikey in self.apikeys:
                self._current_apikey = apikey
                yield CoinMarketCapAPI(apikey)

    @staticmethod
    def _load_db() -> dict:
        if not os.path.exists(DBFILE):
            with open(DBFILE, 'w') as f:
                f.write('{}')

        with open(DBFILE) as f:
            return json.load(f)

    def _update_db(self) -> None:
        with open(DBFILE, 'w') as f:
            json.dump(self.data, f)

    @api_except
    def _get_price(self, symbol, money) -> Optional[Union[float, int]]:  # или Optional[float | int]
        api = next(self.api)
        r = api.cryptocurrency_quotes_latest(symbol=symbol, convert=money)
        price = r.data[symbol][0]['quote'][money]['price']
        if money == 'BTC':
            # Использовать константу
            result = int(price * SATOSHIS_PER_BTC)
        elif money == 'USD':
            result = round(price, 4)
        else:
            raise ValueError(f'Неподдерживаемая валюта: {money}, только BTC и USD')
        return result

    # Убрали coins из аргументов, если читаем из конфига/атрибута класса
    def start(self):
        t = PrettyTable()
        t.field_names = ['Монета', "Текущяя цена", "Рост", "Старая цена"]
        # Использовать атрибут класса или значение из конфига
        coins_to_monitor = MONITOR_COINS  # Загрузить из config, если нужно
        percent_threshold = PERCENT  # Загрузить из config, если нужно

        data_updated = False  # Флаг, указывающий, нужно ли сохранять БД

        for pair_config in coins_to_monitor:
            msg = ''
            notify_status = False
            symbol, money, crop, pair_key = None, None, None, None  # Инициализация

            try:
                # --- Логика парсинга ---
                if '[' in pair_config:
                    base_pair, crop_str = pair_config.split('[')
                    crop = int(crop_str.replace(']', ''))
                    pair_key = base_pair  # Ключ для БД без обрезки
                    symbol, money = base_pair.split('/')
                else:
                    pair_key = pair_config  # Ключ для БД - полная строка
                    symbol, money = pair_config.split('/')
                    crop = None
                # --- Конец парсинга ---

                cur_price_raw = self._get_price(symbol, money)

                # *** Обработка возможной ошибки API (возврат None) ***
                if cur_price_raw is None:
                    log.warning(f"Не удалось получить цену для {pair_key}. Пропуск этого цикла.")
                    # Можно добавить строку-заглушку в таблицу
                    t.add_row([pair_key, "Ошибка API", "N/A", self.data.get(pair_key, "N/A")])
                    continue  # Переход к следующей монете

                # Применить обрезку, если нужно
                cur_price = cur_price_raw
                if crop:
                    # Используем isinstance для проверки типа
                    cur_price = float(str(cur_price_raw)[:crop]) if isinstance(cur_price_raw, float) else int(
                        str(cur_price_raw)[:crop])

                if pair_key == 'BTC/USD':
                    try:
                        # Отбрасываем дробную часть для BTC/USD
                        cur_price = int(cur_price)
                    except (ValueError, TypeError):
                        # Обработка случая, если cur_price не может быть преобразован в int
                        log.error(f"Не удалось преобразовать цену BTC/USD ({cur_price}) в int.")
                        t.add_row([pair_key, "Ошибка типа", "N/A", self.data.get(pair_key, "N/A")])
                        continue  # Пропускаем эту пару, если преобразование не удалось

                # Инициализация БД, если монета новая
                if pair_key not in self.data:
                    log.info(f"Инициализация базовой цены для {pair_key}: {cur_price}")
                    self.data[pair_key] = cur_price
                    # self._update_db() # Переместим обновление в конец цикла
                    data_updated = True
                    # Добавляем начальное состояние в таблицу и пропускаем расчет %
                    t.add_row([pair_key, cur_price, "+0%", cur_price])
                    continue

                old_price = self.data[pair_key]

                # *** Предотвращение ZeroDivisionError ***
                if old_price == 0:
                    if cur_price == 0:
                        raw_change_percent = 0.0
                    else:
                        # Обработать значительное изменение от 0 или пропустить
                        log.warning(f"Старая цена для {pair_key} была 0. Невозможно рассчитать процентное изменение.")
                        # Можно добавить строку и перейти дальше
                        t.add_row([pair_key, cur_price, "N/A (Старая=0)", old_price])
                        continue
                else:
                    # Расчет "сырого" процента для точного сравнения
                    raw_change_percent = ((cur_price - old_price) / old_price) * 100

                # Округленный процент для отображения и логов (если нужно)
                change_percent_display = round(raw_change_percent)

                # Проверка порогов по "сырому" значению
                if raw_change_percent <= -percent_threshold:
                    # Используем emoji и округленное значение для сообщения
                    msg = f"🔻 {pair_key} упала на {abs(change_percent_display)}% [{cur_price}] (Было: {old_price})"
                    notify_status = True
                elif raw_change_percent >= percent_threshold:
                    msg = f"🔼 {pair_key} повысилась на {change_percent_display}% [{cur_price}] (Было: {old_price})"
                    notify_status = True

                if notify_status:
                    log.info(msg)
                    self.notify.send(msg)
                    self.data[pair_key] = cur_price  # Обновляем базу при уведомлении
                    # self._update_db() # Переместим обновление в конец цикла
                    data_updated = True

                # Добавляем строку в таблицу, используя улучшенное форматирование
                percent_str = f"{change_percent_display:+}%"  # Знак + добавится автоматически
                t.add_row([pair_key, cur_price, percent_str, old_price])

            except Exception as e:
                # Ловим другие возможные ошибки при обработке одной монеты
                log.error(f"Ошибка при обработке монеты '{pair_config}': {e}", exc_info=True)
                t.add_row([pair_config, "Ошибка обработки", "N/A", "N/A"])

        # Обновляем файл БД один раз в конце, если были изменения
        if data_updated:
            self._update_db()

        # Вывод
        # os.system('cls' if os.name == 'nt' else 'clear') # Опционально
        print("\n" * 5)  # Можно уменьшить количество пустых строк
        print(t)
        log.debug(f"Проверка завершена: {datetime.now()}")
        time.sleep(SLEEP)  # Пауза остается здесь, т.к. start вызывается в цикле


def main():
    telega = Telega(secret.telegram.chat_crypto)
    monitor = MarketCapMonitor(telega)
    while True:
        monitor.start()


if __name__ == '__main__':
    while True:
        try:
            main()
        except Exception as e:
            log.error(e)
            time.sleep(10)
