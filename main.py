from multiprocessing import Process, Manager, Lock


class WarehouseManager:

    def __init__(self):
        self.data = Manager().dict()
        self.lock = Lock()

    def run(self, requests):
        all_process = []
        for request in requests:
            process = Process(target=self.process_request, args=(request,))
            all_process.append(process)
            process.start()

        for process in all_process:
            process.join()

    def process_request(self, request):
        with self.lock:
            key, act, value = request
            if act == "receipt":
                if key in self.data:
                    self.data[key] += value
                else:
                    self.data[key] = value
            elif act == "shipment":
                if key in self.data:
                    if self.data[key] >= value:
                        self.data[key] -= value
                    else:
                        print(f"Нельзя взять: {value} на складе больше чем имеется:", flush=True)
                else:
                    print(f"{value} нет на складе.", flush=True)


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
    print(manager.data, flush=True)
