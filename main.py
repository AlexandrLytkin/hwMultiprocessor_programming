import threading
from collections import defaultdict


class WarehouseManager(threading.Thread):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = defaultdict(int)

    def run(self, requests):
        self.process_request(requests)

    def process_request(self, request):
        for key, proces, value in request:
            if proces == 'receipt':
                self.data[key] += value
            elif proces == 'shipment':
                self.data[key] -= value


if __name__ == '__main__':
    # Создаем менеджера склада
    manager = WarehouseManager()

    # Множество запросов на изменение данных о складских запасах
    requests = [
        ("product1", "receipt", 100),
        ("product2", "receipt", 150),
        ("product1", "shipment", 30),
        ("product3", "receipt", 200),
        ("product2", "shipment", 50)
    ]

    # Запускаем обработку запросов
    manager.run(requests)

    # Выводим обновленные данные о складских запасах
    print(dict(manager.data))
