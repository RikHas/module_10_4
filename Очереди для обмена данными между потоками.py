import threading
import time
from queue import Queue

class Table:
    def __init__(self, number):
        self.number = number
        self.is_busy = False

class Cafe:
    def __init__(self, tables):
        self.tables = tables
        self.queue = Queue()
        self.customer_id = 1

    def customer_arrival(self):
        for _ in range(20):
            print(f"Посетитель номер {self.customer_id} прибыл.")
            customer_thread = threading.Thread(target=self.serve_customer, args=(self.customer_id,))
            customer_thread.start()
            self.customer_id += 1
            time.sleep(1)

    def serve_customer(self, customer_id):
        available_table = None
        for table in self.tables:
            if not table.is_busy:
                available_table = table
                break

        if available_table:
            available_table.is_busy = True
            print(f"Посетитель номер {customer_id} сел за стол {available_table.number}.")
            customer = Customer(customer_id, available_table)
            customer.start()
        else:
            print(f"Посетитель номер {customer_id} ожидает свободный стол.")
            self.queue.put(customer_id)

    def release_table(self, customer_id, table):
        print(f"Посетитель номер {customer_id} покушал и ушёл.")
        table.is_busy = False
        if not self.queue.empty():
            next_customer_id = self.queue.get()
            print(f"Посетитель номер {next_customer_id} сел за стол {table.number}.")
            customer = Customer(next_customer_id, table)
            customer.start()

class Customer(threading.Thread):
    def __init__(self, customer_id, table):
        super().__init__()
        self.customer_id = customer_id
        self.table = table

    def run(self):
        time.sleep(5)
        cafe.release_table(self.customer_id, self.table)

# Создаем столики в кафе
table1 = Table(1)
table2 = Table(2)
table3 = Table(3)
tables = [table1, table2, table3]

# Инициализируем кафе
cafe = Cafe(tables)

# Запускаем поток для прибытия посетителей
customer_arrival_thread = threading.Thread(target=cafe.customer_arrival)
customer_arrival_thread.start()

# Ожидаем завершения работы прибытия посетителей
customer_arrival_thread.join()
